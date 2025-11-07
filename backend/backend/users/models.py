from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for PlayForward.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    USER_TYPE_CHOICES = (
        ("normal", "Normal User"),
        ("udruga", "Udruga"),
    )

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First name"), blank=True, max_length=255)
    last_name = CharField(_("Last name"), blank=True, max_length=255)
    email = EmailField(_("Email address"), unique=True)
    username = CharField(_("Username"), blank=True, max_length=255)
    type = CharField(_("Type"), max_length=50, blank=True)
    role = CharField(_("Role"), max_length=50, blank=True)
    location = CharField(_("Location"), max_length=50, blank=True)
    registration_step = models.IntegerField(default=0)
    '''user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="normal"
    )'''

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    class Meta:
        permissions = [
            ("can_access_update_role", "Can access update role"),
            ("can_access_update_type", "Can access update type"),
            ("can_access_basic_info", "Can access basic info"),
            ("can_access_udruga_additional_info", "Can access udruga additional info"),
        ]

    '''def save(self, *args, **kwargs):
        if self.user_type == "udruga":
            self.first_name = ""
            self.last_name = ""
        super().save(*args, **kwargs)'''

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization')
    company_name = CharField(_("Company name"), max_length=255)
    company_email = EmailField(_("Company email"), blank=True)

    def __str__(self):
        return self.company_name
