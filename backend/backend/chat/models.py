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

    class Meta:
        unique_together = ('donor', 'recipient', 'listing')

    def __str__(self) -> str:
        return "(" + str(self.channel_id) + ")"

