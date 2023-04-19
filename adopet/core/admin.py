from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from adopet.core.models import CustomUser as User


class UserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("id",)},
        ),
        (
            _("User data"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal info"),
            {"fields": ("name",)},
        ),
        (
            _("User type"),
            {
                "fields": (
                    "is_tutor",
                    "is_shelter",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "modified_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = (
        "id",
        "name",
        "email",
        "is_staff",
        "is_active",
        "is_tutor",
        "is_shelter",
        "created_at",
        "modified_at",
    )
    list_filter = (
        "is_active",
        "is_tutor",
        "is_shelter",
    )

    readonly_fields = (
        "id",
        "last_login",
        "created_at",
        "modified_at",
    )

    search_fields = ("name", "email")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
