from django.urls import path

from .views import CreateStreamToken, CreateChatChannel, CreateDeliveryRequest, RespondDeliveryRequest

app_name = "chat"

urlpatterns = [
    path("", CreateStreamToken.as_view(), name="createStreamToken"),
    path("create/<int:listing_id>/", CreateChatChannel.as_view(), name="createChatChannel"),
    path("delivery/request/<int:listing_id>/", CreateDeliveryRequest.as_view(), name="createRequest"),
    path("delivery/response/<str:msg_id>/", RespondDeliveryRequest.as_view(), name="respondRequest"),
]
