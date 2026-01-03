from django.urls import path
from .views import (
    AppointmentCreateView,
    MyAppointmentsView,
    AppointmentListAdminView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    AppointmentStatusUpdateView,
)

urlpatterns = [
    path("", AppointmentCreateView.as_view()),
    path("me/", MyAppointmentsView.as_view()),
    path("all/", AppointmentListAdminView.as_view()),
    path("<int:pk>/", AppointmentUpdateView.as_view()),
    path("<int:pk>/delete/", AppointmentDeleteView.as_view()),
    path("<int:pk>/status/", AppointmentStatusUpdateView.as_view()),
]
