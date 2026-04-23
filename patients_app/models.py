from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s\-]{7,20}$",
    message="Enter a valid phone number."
)


class Patient(models.Model):
    related_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    phone_number = models.CharField(
        max_length=20,
        validators=[phone_validator],
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='patient_profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return (self.related_user.get_full_name() or self.related_user.username).strip()