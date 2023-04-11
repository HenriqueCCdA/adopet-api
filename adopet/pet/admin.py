from django.contrib import admin

from .models import Adoption, Pet


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


@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pet",
        "tutor",
        "date",
        "is_active",
        "created_at",
        "modified_at",
    )

    list_filter = ("is_active",)

    search_fields = ("pet", "tutor")
