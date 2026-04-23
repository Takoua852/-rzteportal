from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "related_user", "phone_number", "date_of_birth")
    search_fields = ("related_user__username", "related_user__email", "phone_number")