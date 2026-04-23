from rest_framework import serializers
from appointments_app.models import Appointment
from doctors_app.models import Doctor
from patients_app.models import Patient


class AppointmentListSerializer(serializers.ModelSerializer):
    doctor_username = serializers.CharField(
        source="has_doctor.related_user.username", read_only=True)
    patient_username = serializers.CharField(
        source="has_patient.related_user.username", read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "title", "date", "doctor_username", "patient_username"]


class AppointmentDetailSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(
        source="has_doctor.id", read_only=True)
    doctor_username = serializers.CharField(
        source="has_doctor.related_user.username", read_only=True)
    patient_id = serializers.IntegerField(
        source="has_patient.id", read_only=True)
    patient_username = serializers.CharField(
        source="has_patient.related_user.username", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id", "doctor_id", "doctor_username", "patient_id",
            "patient_username", "title", "description", "date", "created_at"
        ]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), required=False, write_only=True)
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), required=False, write_only=True)

    class Meta:
        model = Appointment
        fields = ["doctor", "patient", "title", "description", "date"]

    def validate(self, attrs):
        user = self.context["request"].user
        date = attrs["date"]

        if hasattr(user, "doctor_profile"):
            attrs["has_doctor"] = user.doctor_profile
            if "patient" not in attrs:
                raise serializers.ValidationError(
                    {"patient": "a doctor must specify a patient."})
            attrs["has_patient"] = attrs.pop("patient")

        elif hasattr(user, "patient_profile"):
            attrs["has_patient"] = user.patient_profile
            if "doctor" not in attrs:
                raise serializers.ValidationError(
                    {"doctor": "a patient must specify a doctor."})
            attrs["has_doctor"] = attrs.pop("doctor")
        else:
            raise serializers.ValidationError(
                "User profile (Doctor/Patient) not found.")

        self._check_availability(
            attrs["has_doctor"], attrs["has_patient"], date)

        return attrs

    def _check_availability(self, doctor, patient, date):
        if Appointment.objects.filter(has_doctor=doctor, date=date).exists():
            raise serializers.ValidationError(
                {"date": "The doctor has an appointment at this time."})

        if Appointment.objects.filter(has_patient=patient, date=date).exists():
            raise serializers.ValidationError(
                {"date": "The patient has an appointment at this time."})

    def create(self, validated_data):
        validated_data.pop("doctor", None)
        validated_data.pop("patient", None)
        return Appointment.objects.create(**validated_data)


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["title", "description", "date"]

    def validate_date(self, value):
        appointment = self.instance
        doctor = appointment.has_doctor
        patient = appointment.has_patient

        if Appointment.objects.filter(
            has_doctor=doctor, date=value
        ).exclude(id=appointment.id).exists():
            raise serializers.ValidationError(
                "The doctor has an appointment at this time.")

        if Appointment.objects.filter(
            has_patient=patient, date=value
        ).exclude(id=appointment.id).exists():
            raise serializers.ValidationError(
                "The patient has an appointment at this time.")

        return value
