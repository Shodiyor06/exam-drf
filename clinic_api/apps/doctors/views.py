from rest_framework import generics, filters
from .models import DoctorProfile, TimeSlot
from .serializers import DoctorProfileSerializer, TimeSlotSerializer
from apps.users.permissions import IsDoctor
from rest_framework.permissions import IsAuthenticated

class DoctorListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.select_related("user")
    serializer_class = DoctorProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["specialization", "user__username"]
    permission_classes = [IsAuthenticated]


class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsDoctor]

    def get_object(self):
        return DoctorProfile.objects.get(user=self.request.user)

class DoctorTimeSlotsView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TimeSlot.objects.filter(
            doctor_id=self.kwargs["pk"],
            is_available=True
        )


class TimeSlotCreateView(generics.CreateAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctorprofile)


class MyTimeSlotsView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return TimeSlot.objects.filter(doctor=self.request.user.doctorprofile)
