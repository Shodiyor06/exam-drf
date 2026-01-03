from django.db import models
from apps.users.models import User


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class TimeSlot(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="timeslots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
