from django.contrib import admin

from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "size",
        "age",
        "behavior",
        "is_active",
        "created_at",
        "modified_at",
    )

    list_filter = ("is_active",)

    search_fields = ("name", "email")
    ordering = ("name",)
