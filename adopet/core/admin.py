from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Adoption, Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("id",)},
        ),
        (
            _("Pet Info"),
            {
                "fields": (
                    "name",
                    "photo_tag",
                    "photo",
                    "size",
                    "age",
                    "behavior",
                    "is_adopted",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_active",)},
        ),
        (_("Date"), {"fields": ("created_at", "modified_at")}),
    )

    list_display = (
        "id",
        "name",
        "size",
        "age",
        "behavior",
        "is_active",
        "is_adopted",
        "created_at",
        "modified_at",
    )

    list_filter = ("is_active",)

    readonly_fields = (
        "id",
        "created_at",
        "modified_at",
        "photo_tag",
    )

    search_fields = ("name", "email")
    ordering = ("name",)


@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("id",)},
        ),
        (
            _("Pet Info"),
            {
                "fields": (
                    "pet",
                    "tutor",
                    "date",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_active",)},
        ),
        (_("Date"), {"fields": ("created_at", "modified_at")}),
    )

    list_display = (
        "id",
        "pet",
        "tutor",
        "date",
        "created_at",
        "modified_at",
    )

    list_filter = ("is_active",)

    search_fields = ("pet", "tutor")

    readonly_fields = (
        "id",
        "created_at",
        "modified_at",
    )
