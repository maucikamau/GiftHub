from django.urls import path

from .views import CreateListView

app_name = "listings"

urlpatterns = [
    path("create/", CreateListView.as_view(), name="createListing"),
]
