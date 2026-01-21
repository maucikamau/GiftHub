from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid

from .managers import UserManager

class User(AbstractUser):
    """
    Default custom user model for PlayForward.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    USER_ROLE_CHOICES = (
        ("donor", "Donor"),
        ("recipient", "Recipient"),
        ("recipient_individual", "Recipient Individual"),
        ("recipient_association", "Recipient Association"),
    )

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First name"), blank=True, max_length=255)
    last_name = CharField(_("Last name"), blank=True, max_length=255)
    email = EmailField(_("Email address"), unique=True)
    username = CharField(_("Username"), blank=True, max_length=255)
    # type = CharField(_("Type"), max_length=50, blank=True)
    role = models.CharField(max_length=25, choices=USER_ROLE_CHOICES, blank=True)
    location = models.ForeignKey('LocationCroatia', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    registration_step = models.IntegerField(default=0)
    chat_uid = models.UUIDField(
        default=uuid.uuid4,
        #unique=True, privremeno dok ne popravimo
        editable=False,
    )
    profile_image = models.ImageField(_("User image"), upload_to='profile_images/', blank=True, null=True)
    '''user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="normal"
    )'''

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def assign_role_group_permissions(self):
        """Assign permissions to the user based on their role group."""
        from django.contrib.auth.models import Group

        if not self.role:
            return  # No role assigned

        try:
            group = Group.objects.get(name=self.role)
            self.groups.clear()  # Clear existing groups
            self.groups.add(group)
        except Group.DoesNotExist:
            pass  # Handle the case where the group does not exist

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


class Association(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization')
    association_name = CharField(_("Association name"), max_length=255)
    association_email = EmailField(_("Association email"), blank=True)

    def __str__(self):
        return self.association_name


class LocationCroatia(models.Model):
    cityName = CharField(max_length=100)

    def __str__(self):
        return self.cityName

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
