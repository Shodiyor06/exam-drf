from rest_framework import serializers
from django.utils import timezone
from .models import Appointment
from apps.doctors.models import TimeSlot


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, data):
        timeslot = data["timeslot"]

        if not timeslot.is_available:
            raise serializers.ValidationError("TimeSlot band")

        if timeslot.date < timezone.now().date():
            raise serializers.ValidationError("O‘tmishdagi vaqtga yozib bo‘lmaydi")

        return data

    def create(self, validated_data):
        timeslot = validated_data["timeslot"]
        timeslot.is_available = False
        timeslot.save()
        return super().create(validated_data)


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["id", "timeslot"]

    def validate(self, data):
        user = self.context["request"].user
        slot = data["timeslot"]

        if not slot.is_available:
            raise serializers.ValidationError("TimeSlot band")

        if slot.doctor.user == user:
            raise serializers.ValidationError("Doctor o‘ziga yozila olmaydi")

        return data

    def create(self, validated_data):
        slot = validated_data["timeslot"]
        slot.is_available = False
        slot.save()

        return Appointment.objects.create(
            doctor=slot.doctor.user,
            patient=self.context["request"].user,
            timeslot=slot,
            status="pending"
        )


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["status"]

    def validate_status(self, value):
        if value not in ["approved", "cancelled", "completed"]:
            raise serializers.ValidationError("Noto‘g‘ri status")
        return value