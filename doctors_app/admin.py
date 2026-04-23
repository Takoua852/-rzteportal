from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "related_user", "title", "specialty", "phone_number")
    search_fields = ("related_user__username", "related_user__email", "specialty")
    list_filter = ("specialty",)