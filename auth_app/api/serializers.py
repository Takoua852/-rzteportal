from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from doctors_app.models import Doctor
from patients_app.models import Patient


class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["doctor", "patient"])
    title = serializers.ChoiceField(
        choices=Doctor.TitleChoices.choices,
        required=False,
        allow_blank=True
    )
    specialty = serializers.ChoiceField(
        choices=Doctor.SpecialtyChoices.choices,
        required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "repeated_password",
            "role",
            "title",
            "specialty",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        repeated_password = attrs.get("repeated_password")
        role = attrs.get("role")
        specialty = attrs.get("specialty")

        if password != repeated_password:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        if User.objects.filter(email=attrs.get("email")).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )

        if role == "doctor" and not specialty:
            raise serializers.ValidationError(
                {"specialty": "Specialty is required for doctors."}
            )

        validate_password(password)
        return attrs

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        role = validated_data.pop("role")
        title = validated_data.pop("title", "")
        specialty = validated_data.pop("specialty", None)

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        if role == "doctor":
            Doctor.objects.create(
                related_user=user,
                title=title,
                specialty=specialty
            )
        elif role == "patient":
            Patient.objects.create(
                related_user=user
            )

        return user