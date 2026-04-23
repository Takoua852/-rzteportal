from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s\-]{7,20}$",
    message="Enter a valid phone number."
)


class Doctor(models.Model):
    class TitleChoices(models.TextChoices):
        DR = "dr", "Dr."
        PROF_DR = "prof_dr", "Prof. Dr."
        MR = "mr", "Mr."
        MS = "ms", "Ms."

    class SpecialtyChoices(models.TextChoices):
        GENERAL_PRACTITIONER = 'GP', 'General Practitioner'
        CARDIOLOGIST = 'CARD', 'Cardiologist'
        DERMATOLOGIST = 'DERM', 'Dermatologist'
        PEDIATRICIAN = 'PED', 'Pediatrician'
        PSYCHIATRIST = 'PSY', 'Psychiatrist'
        ORTHOPEDIST = 'ORTHO', 'Orthopedist'
        GYNECOLOGIST = 'GYNE', 'Gynecologist'
        NEUROLOGIST = 'NEURO', 'Neurologist'
        ONCOLOGIST = 'ONC', 'Oncologist'
        ENDOCRINOLOGIST = 'ENDO', 'Endocrinologist'

    related_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )

    title = models.CharField(
        max_length=20,
        choices=TitleChoices.choices,
        default=TitleChoices.DR)

    specialty = models.CharField(
        max_length=50,
        choices=SpecialtyChoices.choices
    )

    phone_number = models.CharField(
        max_length=20,
        validators=[phone_validator], blank=True
    )
    profile_image = models.ImageField(
        upload_to='doctor_profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        name = self.related_user.get_full_name() or self.related_user.username
        title = self.get_title_display() if self.title else ""
        return f"{title} {name} - {self.get_specialty_display()}".strip()
