import uuid
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from backend import users, listings


class ChatChannel(models.Model):
    stream_channel_id = models.CharField(_('channel_id'), max_length=100, unique=True)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='chats')
    donor = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='donor_chats')
    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recipient_chats')
    delivery_check = models.BooleanField(_('delivery_check'), default=False)
    delivery_chat_id = models.CharField(_('delivery_chat_id'), max_length=100, unique=True, blank=True, null=True)
    delivery_type = models.CharField(_('delivery_type'), max_length=50, blank=True, null=True)
    delivery_accepted = models.BooleanField(_('delivery_accepted'), default=False)
    delivery_price = models.DecimalField(_('delivery_price'), max_digits=5, default=0.00)

    class Meta:
        unique_together = ('donor', 'recipient', 'listing')

    def __str__(self) -> str:
        return "(" + str(self.stream_channel_id) + ")"

