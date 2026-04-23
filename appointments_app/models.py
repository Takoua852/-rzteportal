from django.db import models
from doctors_app.models import Doctor
from patients_app.models import Patient


class Appointment(models.Model):
    has_doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointments")
    has_patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        constraints = [
            models.UniqueConstraint(
                fields=['has_doctor', 'has_patient', 'date'],
                name='unique_appointment_doctor_patient_date'
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.date}"
