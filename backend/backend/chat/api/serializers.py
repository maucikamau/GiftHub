from rest_framework import serializers
from ..models import ChatChannel
from ...users.api.serializers import LocationSerializer
from ...users.models import User, LocationCroatia

class ChatChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatChannel
        fields = ["id", "stream_channel_id", "listing", "donor", "recipient"]
