from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView
from stream_chat import StreamChat
from backend.chat.models import ChatChannel
from backend.chat.utils import get_or_create_chat_channel
from backend.listings.models import Listing


class CreateChatChannel(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        listing_id = kwargs['listing_id']  # From URL path

        chat_channel = get_or_create_chat_channel(listing_id, request.user)

        return Response({
            "id": chat_channel.id,
            "stream_channel_id": chat_channel.stream_channel_id,
            "listing_id": chat_channel.listing.id,
        }, status=status.HTTP_201_CREATED)

class CreateDeliveryRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        listing_id = kwargs['listing_id']
        delivery_type = request.data.get('delivery_type')

        if not Listing.objects.filter(id=listing_id).exists():
            return Response({"detail": "Oglas ne postoji."}, status=404)
        recipient = request.user

        client = StreamChat(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)
        channel_id = f"{listing_id}-{recipient.chat_uid}"

        chat = get_or_create_chat_channel(listing_id, recipient)
        if chat.delivery_check:
            return Response({"detail": "Zahtjev za dostavu je već poslan."}, status=400)

        channel = client.channel("messaging", channel_id)
        message = {
            "text": f"Zahtjev za dostavu ({delivery_type})",
            "type": "system",
            "messageType": "DonationRequest",
            "delivery_type": delivery_type
        }

        message_response = channel.send_message(message, recipient.chat_uid)
        request_id = message_response['message']['id']  # ✅ "msg-123-abc456"
        chat.delivery_request_msg_id = request_id
        chat.delivery_type = delivery_type
        chat.delivery_check = True

        chat.save()
        return Response({"detail": "Zahtjev za dostavu je uspješno poslan."}, status=200)

class RespondDeliveryRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        msg_id = kwargs['msg_id']
        check = request.data.get('check')

        if 'check' not in request.data:
            return Response({"detail": "Nedostaje parametar 'check'."}, status=400)

        chat = get_object_or_404(ChatChannel, delivery_request_msg_id=msg_id)

        client = StreamChat(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)
        if not chat.delivery_check:
            return Response({"detail": "Zahtjev za dostavu ne postoji."}, status=400)
        if chat.delivery_accepted:
            return Response({"detail": "Zahtjev za dostavu je već prihvaćen."}, status=400)

        updates = {}
        if check == False:
            chat.delivery_check = False
            chat.delivery_accepted = False
            chat.delivery_type = None
            chat.delivery_request_msg_id = None

            updates['status'] = 'rejected'
        else:
            chat.delivery_accepted = True
            updates['status'] = 'accepted'

        client.update_message_partial(msg_id, {"set": updates}, 'gifthub')
        channel = client.channel("messaging", chat.stream_channel_id)
        channel.update_partial(to_set={"delivery_accepted": chat.delivery_accepted})

        chat.save()

        if check == False:
            return Response({"detail": "Zahtjev za dostavu je odbijen."}, status=200)

        return Response({"detail": "Zahtjev za dostavu je prihvaćen."}, status=200)


class CreateStreamToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        client = StreamChat(
            api_key=settings.STREAM_API_KEY,
            api_secret=settings.STREAM_API_SECRET
        )

        user = request.user

        # Prepare user data for Stream
        user_data = {
            "id": user.chat_uid,
            "name": user.username,
        }

        # Create/update user in Stream
        client.upsert_user(user_data)

        # Generate Stream token (valid 1 hour)
        token = client.create_token(user.chat_uid)

        # Return everything frontend needs
        return Response({
            "api_key": settings.STREAM_API_KEY,
            "user_id": str(user.chat_uid),
            "token": token,
        })
