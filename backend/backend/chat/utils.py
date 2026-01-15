from django.conf import settings
from django.shortcuts import get_object_or_404
from stream_chat import StreamChat

from backend.chat.models import ChatChannel
from backend.listings.models import Listing


def get_or_create_chat_channel(listing_id, recipient):
    listing = get_object_or_404(Listing, id=listing_id)
    donor = listing.owner

    channel_id = f"{listing_id}-{recipient.chat_uid}"

    if ChatChannel.objects.filter(stream_channel_id=channel_id).exists():
        return ChatChannel.objects.get(stream_channel_id=channel_id)

    client = StreamChat(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)
    channel_data = {
        'name': f"{donor.username}",
        'listingId': listing_id,
        'members': [str(donor.chat_uid), str(recipient.chat_uid)]
    }

    channel = client.channel('messaging', channel_id, channel_data)
    channel.create(str(recipient.id))

    return ChatChannel.objects.create(
        stream_channel_id=channel_id,
        listing=listing,
        donor=donor,
        recipient=recipient,
    )
