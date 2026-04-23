from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDoctorOwnerOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return obj.related_user == request.user