from rest_framework import serializers
from doctors_app.models import Doctor


class DoctorListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='related_user.username', read_only=True)
    title_display = serializers.CharField(source='get_title_display', read_only=True)
    specialty_display = serializers.CharField(source='get_specialty_display', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id",
            "username",
            "title",
            "title_display",
            "specialty",
            "specialty_display",
            "profile_image",
        ]


class DoctorDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='related_user.username', read_only=True)
    email = serializers.EmailField(source='related_user.email', read_only=True)
    title_display = serializers.CharField(source='get_title_display', read_only=True)
    specialty_display = serializers.CharField(source='get_specialty_display', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id",
            "related_user",
            "username",
            "email",
            "title",
            "title_display",
            "specialty",
            "specialty_display",
            "phone_number",
            "profile_image",
        ]
        read_only_fields = ["id", "related_user", "username", "email"]


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "title",
            "specialty",
            "phone_number",
            "profile_image",
        ]