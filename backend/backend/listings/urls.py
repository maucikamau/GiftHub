from django.urls import path

from .views import CreateListView, ListingsListView, ListingsMeView, ListingsSpecificView

app_name = "listings"

urlpatterns = [
    path("", ListingsListView.as_view(), name="allListings"),
    path("create/", CreateListView.as_view(), name="createListing"),
    path("me/", ListingsMeView.as_view(), name="myListings"),
    path("<int:pk>/", ListingsSpecificView.as_view(), name="pkListings"),
]
