from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from stream_chat import StreamChat
from backend.chat.api.serializers import ChatChannelSerializer
from backend.chat.models import ChatChannel
from backend.listings.models import Listing
from backend.users.models import User


class CreateChatChannel(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        listing_id = kwargs['listing_id']  # From URL path

        listing = get_object_or_404(Listing, id=listing_id)
        recipient = request.user
        donor = listing.owner

        channel_id = f"{listing_id}-{recipient.chat_uid}"

        if ChatChannel.objects.filter(stream_channel_id=channel_id).exists():
            chat = ChatChannel.objects.get(stream_channel_id=channel_id)
            return Response(self.get_serializer(chat).data, status=200)

        client = StreamChat(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)
        channel_data = {
            'name': f"{donor.username}",
            'listingId': listing_id,
            'members': [str(donor.chat_uid), str(recipient.chat_uid)]
        }

        channel = client.channel('messaging', channel_id, channel_data)
        channel.create(str(recipient.id))

        chat_channel = ChatChannel.objects.create(
            stream_channel_id=channel_id,
            listing=listing,
            donor=donor,
            recipient=recipient,
        )

        serializer = self.get_serializer(chat_channel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateDeliveryRequest(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        listing_id = kwargs['listing_id']
        delivery_type = request.data.get('delivery_type')

        listing = get_object_or_404(Listing, id=listing_id)
        recipient = request.user

        client = StreamChat(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)
        channel_id = f"{listing_id}-{recipient.chat_uid}"

        channel_data = {
            'name': f"{listing.owner.username}-{recipient.username}",
            'listingId': listing_id,
            'members': [str(listing.owner.chat_uid), str(recipient.chat_uid)]
        }

        if ChatChannel.objects.filter(stream_channel_id=channel_id).exists():
            chat = ChatChannel.objects.get(stream_channel_id=channel_id)
            if chat.delivery_check:
                return Response({"detail": "Zahtjev za dostavu je već poslan."}, status=400)
            else:
                chat.delivery_check = True
                chat.save()

        else:
            return Response({"detail": "Chat kanal ne postoji."}, status=404)

        channel = client.channel("messaging", channel_id, channel_data)
        message = {
            "text": f"Zahtjev za dostavu ({delivery_type}).",
            "type": "system",
            "delivery_type": delivery_type
        }

        chat = ChatChannel.objects.get(stream_channel_id=channel_id)
        message_response = channel.send_message(message, recipient.chat_uid)
        request_id = message_response['message']['id']  # ✅ "msg-123-abc456"
        chat.delivery_id = request_id
        chat.delivery_type = delivery_type

        chat.save()
        return Response({"detail": "Zahtjev za dostavu je uspješno poslan."}, status=200)

class CreateStreamToken(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create_token(self, *args, **kwargs):
        client = StreamChat(
            api_key="settings.STREAM_API_KEY",  #nisam siguran kako sigurno ove podatke staviti
            api_secret="settings.STREAM_API_SECRET"
        )

        user = self.request.user

        # 3. Prepare user data for Stream
        user_data = {
            "id": user.chat_uid,
            "name": user.username,
        }

        # 4. Create/update user in Stream
        client.upsert_user(user_data)

        # 5. Generate Stream token (valid 1 hour)
        token = client.create_token(user.chat_uid)

        # 6. Return everything frontend needs
        return Response({
            "api_key": settings.STREAM_API_KEY,
            "user_id": user.chat_uid,
            "token": token,
        })
