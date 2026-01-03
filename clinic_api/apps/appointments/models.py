from django.db import models
from apps.users.models import User
from apps.doctors.models import DoctorProfile
from apps.doctors.models import TimeSlot



class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    timeslot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
