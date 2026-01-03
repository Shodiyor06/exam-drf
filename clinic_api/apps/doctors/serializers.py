from rest_framework import serializers
from .models import DoctorProfile, TimeSlot


class DoctorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "username",
            "specialization",
            "experience_years",
            "gender",
        ]


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"

    def validate(self, data):
        qs = TimeSlot.objects.filter(
            doctor=data["doctor"],
            date=data["date"],
            start_time__lt=data["end_time"],
            end_time__gt=data["start_time"],
        )
        if qs.exists():
            raise serializers.ValidationError("Bu vaqtda boshqa slot bor")
        return data

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "username",
            "specialization",
            "experience_years",
            "gender",
        ]


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"

    def validate(self, data):
        doctor = data["doctor"]
        date = data["date"]
        start = data["start_time"]
        end = data["end_time"]

        if start >= end:
            raise serializers.ValidationError("Start va end vaqt noto‘g‘ri")

        qs = TimeSlot.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lt=end,
            end_time__gt=start
        )
        if qs.exists():
            raise serializers.ValidationError("Bu vaqt oralig‘i band")

        return data
