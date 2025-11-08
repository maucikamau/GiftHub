from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.models import Session
from allauth.socialaccount.admin import SocialAccountAdmin, SocialAppAdmin
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
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
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
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]

admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.register(Session)

@admin.register(SocialAccount)
class SocialAccountAdminCustom(SocialAccountAdmin, ModelAdmin):
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
