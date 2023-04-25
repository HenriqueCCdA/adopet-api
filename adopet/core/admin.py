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
                    "shelter",
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
        "shelter",
        "is_active",
        "is_adopted",
        "created_at",
        "modified_at",
    )

    list_filter = ("is_active", "size", "is_adopted")

    readonly_fields = (
        "id",
        "created_at",
        "modified_at",
        "photo_tag",
    )

    search_fields = ("name", "shelter")
    ordering = ("name",)

    actions = ("make_active", "make_disable")

    @admin.action(description="Mark selected entries as active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected entries as disable")
    def make_disable(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("id", "shelter")},
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
        "shelter",
        "tutor",
        "date",
        "created_at",
        "modified_at",
    )

    list_filter = ("is_active",)

    search_fields = ("pet", "tutor")

    readonly_fields = (
        "id",
        "shelter",
        "created_at",
        "modified_at",
    )

    def shelter(self, obj):
        return obj.pet.shelter
