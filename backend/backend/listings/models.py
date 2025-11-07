from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from .. import users


# Create your models here.
class Listing(models.Model):
    title = models.CharField(_('title'), max_length=100)
    content = models.TextField(_('content'))
    picture = models.ImageField(_('picture'), upload_to='listing_pictures/', blank=True, null=True)
    category = models.CharField(_('category'), max_length=50)
    status = models.CharField(_('status'), max_length=50)
    location = models.CharField(_('location'), max_length=50)
    delivery = models.CharField(_('payment'), max_length=50)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='listings')

    REQUIRED_FIELDS = []

    def get_absolute_url(self) -> str:
        """Get URL for listing's detail view.

        Returns:
            str: URL for listing detail.

        """
        return reverse("listings:detail", kwargs={"pk": self.id})
