from django.urls import path

from .views import CreateStreamToken

app_name = "chat"

urlpatterns = [
    path("", CreateStreamToken.as_view(), name="createStreamToken"),
]
