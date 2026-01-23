from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


# Create your models here.
class Campaign(models.Model):

    title = models.CharField(_('title'), max_length=100)
    picture = models.ImageField(_('picture'), upload_to='campaign_pictures/', blank=True, null=True)
    description = models.TextField(_('description'))
    location = models.ForeignKey('users.LocationCroatia', null=True, blank=True, on_delete=models.SET_NULL, related_name='campaigns')
    wish_list = models.JSONField(
        _('wish_list'),
        default=list,
    )
    end_date = models.DateTimeField(_('end date'), null=True, blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='campaigns')
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if self.wish_list:
            names = [item['name'] for item in self.wish_list]
            if len(names) != len(set(names)):
                raise ValidationError({
                    'wish_list': _('Duplicate toy names are not allowed in the wish list.')
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for campaigns detail view.

        Returns:
            str: URL for campaigns detail.

        """
        return reverse("campaigns:detail", kwargs={"pk": self.id})
