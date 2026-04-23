from rest_framework import generics, permissions
from doctors_app.models import Doctor
from .serializers import DoctorListSerializer, DoctorDetailSerializer, DoctorUpdateSerializer
from .permissions import IsDoctorOwnerOrAuthenticatedReadOnly


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.select_related("related_user").all()
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.select_related("related_user").all()
    permission_classes = [IsDoctorOwnerOrAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DoctorDetailSerializer
        return DoctorUpdateSerializer

    def perform_update(self, serializer):
        doctor = self.get_object()
        if doctor.related_user != self.request.user:
            raise permissions.PermissionDenied("You can only update your own doctor profile.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.related_user != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own doctor profile.")
        instance.delete()