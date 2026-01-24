from django.urls import path

from .views import CreateListingView, UpdateListingView, ListingsListView, ListingsMeView, ListingsSpecificView, \
    ListingsBulkView, ActiveDonationsView, ConfirmDeliveryView, CancelDonationView

app_name = "listings"

urlpatterns = [
    path("", ListingsListView.as_view(), name="allListings"),
    path("create/", CreateListingView.as_view(), name="createListing"),
    path("update/<int:pk>/", UpdateListingView.as_view(), name="updateListing"),
    path("me/", ListingsMeView.as_view(), name="myListings"),
    path("active-donations/", ActiveDonationsView.as_view(), name="activeDonations"),
    path("<int:pk>/confirm-delivery/", ConfirmDeliveryView.as_view(), name="confirmArrival"),
    path("<int:pk>/cancel-donation/", CancelDonationView.as_view(), name="cancelDonation"),
    path("<int:pk>/", ListingsSpecificView.as_view(), name="pkListings"),
    path("bulk/", ListingsBulkView.as_view(), name="bulkListings"),
]
