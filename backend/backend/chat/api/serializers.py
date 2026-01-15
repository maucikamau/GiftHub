from rest_framework import serializers
from backend.chat.models import ChatChannel

class ChatChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatChannel
        fields = ["id", "stream_channel_id", "listing", "donor", "recipient",
                    "delivery_check", "delivery_chat_id", "delivery_type", "delivery_accepted", "delivery_price"]

