from django.db.models import CharField
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

    LISTING_STATUS_CHOICES = (
        ('available', 'Dostupno'),
        ('accepted_donation', 'Prihvaćena donacija'),
        ('payment_requested', 'Zatražena uplata za dostavu'),
        ('waiting_for_pickup', 'Čeka potvrdu primopredaje'),
        ('completed', 'Završeno'),
    )

    title = models.CharField(_('title'), max_length=100)
    content = models.TextField(_('content'))
    picture = models.ImageField(_('picture'), upload_to='listing_pictures/', blank=True, null=True)
    category = models.CharField(_('category'), max_length=50)
    condition = models.CharField(_('condition'), choices=CONDITION_CHOICES, default="new", null=True, max_length=50)
    location = models.ForeignKey('users.LocationCroatia', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='listings')
    delivery = models.CharField(_('Delivery options'), choices=DELIVERY_CHOICES, max_length=50)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='listings')
    confirmed_donation_conversation = models.OneToOneField('chat.ChatChannel', null=True, blank=True,
                                                                  on_delete=models.SET_NULL,
                                                                  related_name='confirmed_donation_listing')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_active = models.BooleanField(_('is active'), default=True)
    status = models.CharField(_('status'), max_length=50, default='available', choices=LISTING_STATUS_CHOICES)

    def __str__(self) -> str:
        return self.title + " by @" + str(self.owner)

    def get_absolute_url(self) -> str:
        """Get URL for listing's detail view.

        Returns:
            str: URL for listing detail.

        """
        return reverse("listings:detail", kwargs={"pk": self.id})


class ProductCategory(models.Model):
    categoryName = CharField(max_length=100)

    def __str__(self):
        return self.categoryName

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
