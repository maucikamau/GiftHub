from django.utils.translation import gettext_lazy as _
from django.db import models


class ChatChannel(models.Model):
    stream_channel_id = models.CharField(_('channel_id'), max_length=100, unique=True)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='chats')
    donor = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='donor_chats')
    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recipient_chats')
    delivery_check = models.BooleanField('Requested delivery', default=False)
    delivery_request_msg_id = models.CharField('Delivery request message ID', max_length=100, unique=True, blank=True, null=True)
    delivery_type = models.CharField('Requested delivery type', max_length=50, blank=True, null=True)
    delivery_accepted = models.BooleanField('Delivery accepted', default=False)
    payment = models.OneToOneField('payments.Payment', on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_channel')

    class Meta:
        unique_together = ('donor', 'recipient', 'listing')

    def __str__(self) -> str:
        return "(" + str(self.stream_channel_id) + ")"
