from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from adopet.core.managers import UserManager


class CreationModificationBase(models.Model):
    created_at = models.DateTimeField(_("Creation Date and Time"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modificatioin Date and Time"), auto_now=True)

    class Meta:
        abstract = True


class CustomUser(CreationModificationBase, AbstractBaseUser, PermissionsMixin):
    """
    App base User class.
    Email and password are required. Other fields are optional.
    """

    class Role(models.TextChoices):
        TUTOR = "T", "Tutor"
        SHELTER = "S", "Abrigo"

    name = models.CharField("Nome completo", max_length=120)
    email = models.EmailField("Email", unique=True)

    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("Ativo", default=True)

    role = models.CharField("Cargos", max_length=1, choices=Role.choices, null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = False
        ordering = ("-created_at",)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email
