from django.urls import path

from .views import CreateStreamToken, CreateChatChannel, CreateDeliveryRequest

app_name = "chat"

urlpatterns = [
    path("", CreateStreamToken.as_view(), name="createStreamToken"),
    path("create/<int:listing_id>/", CreateChatChannel.as_view(), name="createChatChannel"),
    path("request/delivery/<int:listing_id>/", CreateDeliveryRequest.as_view(), name="createRequest"),
]
