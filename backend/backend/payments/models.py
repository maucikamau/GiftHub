from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class StripeConnectedAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stripe_connected_account'
    )
    stripe_account_id = models.CharField(max_length=255, unique=True)
    charges_enabled = models.BooleanField(default=False)
    payouts_enabled = models.BooleanField(default=False)
    details_submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Stripe Connected Account")
        verbose_name_plural = _("Stripe Connected Accounts")

    def __str__(self):
        return f"{self.user.email} - {self.stripe_account_id}"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    )
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments_received_as_donor',
        help_text='The donor receiving the payment for delivery'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments_made_as_recipient',
        help_text='The recipient paying for the delivery'
    )
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        help_text='The listing being delivered'
    )
    name = models.CharField(max_length=255, help_text='Name for the payment')
    stripe_payment_id = models.CharField(max_length=255, unique=True)
    pay_url = models.URLField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Delivery cost amount')
    currency = models.CharField(max_length=3, default='eur')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for {self.donor.get_full_name()} - {self.name} ({self.amount} {self.currency})"
