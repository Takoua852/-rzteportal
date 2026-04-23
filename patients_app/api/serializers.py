from rest_framework import serializers
from patients_app.models import Patient
from django.contrib.auth.models import User

class PatientListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='related_user.username', read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "username",
            "profile_image",
        ]


class PatientDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='related_user.username', read_only=True)
    email = serializers.EmailField(source='related_user.email', read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "related_user",
            "username",
            "email",
            "phone_number",
            "date_of_birth",
            "profile_image",
        ]
        read_only_fields = ["id", "related_user", "username", "email"]


class PatientUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = Patient
        fields = [
            "phone_number",
            "date_of_birth",
            "profile_image",
            "email"
        ]
    def update(self, instance, validated_data):
        email = validated_data.pop("email", None)

        instance = super().update(instance, validated_data)

        if email is not None:
            instance.related_user.email = email
            instance.related_user.save()

        return instance