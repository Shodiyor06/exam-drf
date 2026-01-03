from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import AppointmentSerializer
from apps.users.permissions import IsPatient, IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import UpdateAPIView
from .serializers import AppointmentStatusSerializer
from apps.users.permissions import IsDoctor


class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsPatient]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patientprofile)


class MyAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return Appointment.objects.filter(doctor=user.doctorprofile)
        if user.role == "patient":
            return Appointment.objects.filter(patient=user.patientprofile)
        return Appointment.objects.none()


class AppointmentListAdminView(generics.ListAPIView):
    queryset = Appointment.objects.select_related("doctor", "patient", "timeslot")
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdmin]


class AppointmentUpdateView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


class AppointmentDeleteView(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

class AppointmentStatusUpdateView(UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentStatusSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_update(self, serializer):
        appointment = self.get_object()

        if appointment.doctor != self.request.user:
            raise PermissionDenied("Bu appointment sizga tegishli emas")

        new_status = serializer.validated_data["status"]

        if new_status == "cancelled":
            appointment.timeslot.is_available = True
            appointment.timeslot.save()

        serializer.save()
