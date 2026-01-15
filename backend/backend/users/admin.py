from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from allauth.socialaccount.admin import SocialAccountAdmin
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.db import models
from typing import List
from django import forms
from unfold.contrib.forms.widgets import WysiwygWidget
from allauth.socialaccount import providers

from unfold.widgets import UnfoldAdminSelectWidget
from unfold.forms import AdminPasswordChangeForm
from unfold.admin import ModelAdmin

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User, Association, LocationCroatia


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": (
            "username",
            ("first_name", "last_name"),
            ("role", "chat_uid"),
            ("location", "registration_step"))}),
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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "_role"]
    search_fields = ["name"]
    ordering = ["id"]
    readonly_fields = ["chat_uid"]


    def _role(self, obj: User) -> str:
        if obj.is_superuser:
            return format_html("<strong>Administrator</strong>")
        # find friendly name for role
        role_dict = dict(obj.USER_ROLE_CHOICES)
        return format_html(role_dict.get(obj.role, "<i>Incomplete Registration</i>"))

    _role.short_description = "Role"


admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)


@admin.register(SocialAccount)
class SocialAccountAdminCustom(SocialAccountAdmin, ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(auth_admin.GroupAdmin, ModelAdmin):
    pass

@admin.register(EmailAddress)
class GroupAdmin(EmailAddressAdmin, ModelAdmin):
    pass

class SocialAppForm(forms.ModelForm):
    class Meta:
        model = SocialApp
        exclude: List[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["provider"] = forms.ChoiceField(
            choices=providers.registry.as_choices(),
            widget=UnfoldAdminSelectWidget,
        )


@admin.register(SocialApp)
class SocialAccountAdminCustom(ModelAdmin):
    form = SocialAppForm

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }


@admin.register(Association)
class AssociationAdmin(ModelAdmin):
    list_display = ["association_name", "association_email", "user"]
    search_fields = ["association_email", "user"]

@admin.register(LocationCroatia)
class LocationCroatiaAdmin(ModelAdmin):
    list_display = ["cityName"]
    search_fields = ["cityName"]
