from rest_framework import generics, permissions
from appointments_app.models import Appointment
from .serializers import (
    AppointmentListSerializer,
    AppointmentDetailSerializer,
    AppointmentCreateSerializer,
    AppointmentUpdateSerializer
)
from .permissions import IsAppointmentOwner


class AppointmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Appointment.objects.select_related(
            "has_doctor__related_user",
            "has_patient__related_user"
        )

        if hasattr(user, "doctor_profile"):
            return queryset.filter(has_doctor=user.doctor_profile)

        if hasattr(user, "patient_profile"):
            return queryset.filter(has_patient=user.patient_profile)

        return queryset.none()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AppointmentCreateSerializer
        return AppointmentListSerializer


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAppointmentOwner]

    def get_queryset(self):
        return Appointment.objects.select_related(
            "has_doctor__related_user",
            "has_patient__related_user"
        )

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return AppointmentUpdateSerializer
        return AppointmentDetailSerializer
