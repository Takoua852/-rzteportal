from rest_framework import generics, permissions
from patients_app.models import Patient
from .serializers import PatientListSerializer, PatientDetailSerializer, PatientUpdateSerializer
from .permissions import IsPatientOwnerOnly
from rest_framework.response import Response


class PatientListView(generics.ListAPIView):
    serializer_class = PatientListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.select_related("related_user").filter(
            related_user=self.request.user
        )


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.select_related("related_user").all()
    permission_classes = [IsPatientOwnerOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PatientUpdateSerializer
        return PatientDetailSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = PatientDetailSerializer(instance)
        return Response(response_serializer.data)
