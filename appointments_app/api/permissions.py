from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAppointmentOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(user, "doctor_profile"):
            return obj.has_doctor == user.doctor_profile

        if hasattr(user, "patient_profile"):
            return obj.has_patient == user.patient_profile

        return False