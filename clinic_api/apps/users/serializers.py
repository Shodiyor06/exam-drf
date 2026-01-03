from rest_framework import serializers
from .models import User
from apps.doctors.models import DoctorProfile
from apps.appointments.models import PatientProfile

from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["doctor", "patient"])
    experience_years = serializers.IntegerField(
        required=False, write_only=True
    )

    class Meta:
        model = User
        fields = ("username", "password", "role", "experience_years")

    def create(self, validated_data):
        role = validated_data.pop("role")
        experience_years = validated_data.pop("experience_years", None)

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        if role == "doctor":
            DoctorProfile.objects.create(
                user=user,
                experience_years=experience_years
            )
        else:
            PatientProfile.objects.create(user=user)

        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "role", "is_active")
