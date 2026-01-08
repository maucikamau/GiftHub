from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from stream_chat import StreamChat

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
