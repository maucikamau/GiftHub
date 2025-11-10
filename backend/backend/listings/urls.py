from django.urls import path

from .views import CreateListingView, UpdateListingView, ListingsListView, ListingsMeView, ListingsSpecificView

app_name = "listings"

urlpatterns = [
    path("", ListingsListView.as_view(), name="allListings"),
    path("create/", CreateListingView.as_view(), name="createListing"),
    path("update/", UpdateListingView.as_view(), name="updateListing"),
    path("me/", ListingsMeView.as_view(), name="myListings"),
    path("<int:pk>/", ListingsSpecificView.as_view(), name="pkListings"),
]
