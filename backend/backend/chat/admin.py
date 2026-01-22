from django.contrib import admin
from unfold.admin import ModelAdmin

from backend.chat.models import ChatChannel


# Register your models here.

@admin.register(ChatChannel)
class ChatChannelAdmin(ModelAdmin):
    list_display = ('stream_channel_id', 'listing', 'donor', 'recipient', 'delivery_check', 'delivery_type', 'delivery_accepted', 'payment')
    search_fields = ('stream_channel_id', 'listing__id', 'donor__username', 'recipient__username')
    list_filter = ('delivery_check', 'delivery_accepted')
