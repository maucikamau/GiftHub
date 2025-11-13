from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.
class Listing(models.Model):

    CONDITION_CHOICES = (
        ("new", "Novo"),
        ("used", "Rabljeno"),
        ("refurbished", "Obnovljeno"),
    )

    DELIVERY_CHOICES = (
        ('pickup', 'Osobno preuzimanje'),
        ('shipping', 'Dostava o trošku primatelja'),
    )

    title = models.CharField(_('title'), max_length=100)
    content = models.TextField(_('content'))
    picture = models.ImageField(_('picture'), upload_to='listing_pictures/', blank=True, null=True)
    category = models.CharField(_('category'), max_length=50)
    condition = models.CharField(_('condition'), choices=CONDITION_CHOICES, default="new", null=True, max_length=50)
    location = models.ForeignKey('users.LocationCroatia', null=True, blank=True, on_delete=models.SET_NULL, related_name='listings')
    delivery = models.CharField(_('Delivery options'), choices=DELIVERY_CHOICES, max_length=50)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='listings')
    REQUIRED_FIELDS = []

    def get_absolute_url(self) -> str:
        """Get URL for listing's detail view.

        Returns:
            str: URL for listing detail.

        """
        return reverse("listings:detail", kwargs={"pk": self.id})
