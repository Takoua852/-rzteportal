from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "has_doctor", "has_patient", "date", "created_at")
    search_fields = (
        "title",
        "has_doctor__related_user__username",
        "has_patient__related_user__username",
    )
    list_filter = ("date", "created_at")