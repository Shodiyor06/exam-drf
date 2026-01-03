from django.urls import path
from .views import (
    DoctorListView,
    DoctorProfileView,
    DoctorTimeSlotsView,
    TimeSlotCreateView,
    MyTimeSlotsView,
)

urlpatterns = [
    path("", DoctorListView.as_view()),
    path("profile/", DoctorProfileView.as_view()),
    path("<int:pk>/timeslots/", DoctorTimeSlotsView.as_view()),

    path("timeslots/", MyTimeSlotsView.as_view()),
    path("timeslots/create/", TimeSlotCreateView.as_view()),
]
