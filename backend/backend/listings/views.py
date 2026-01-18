from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from backend.listings.api.serializers import ListingSerializer, ListingInputSerializer
from backend.listings.models import Listing
from backend.listings.permissions import IsOwnerOrReadOnly, CanCreateListing


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'perPage'
    max_page_size = 1000


class CreateListingView(generics.CreateAPIView):
    queryset = Listing.objects.all()  # pregledava da ne napravimo duplikata
    serializer_class = ListingInputSerializer  # javlja viewu koje podatke trebamo prihvatiti za novog korisnika
    permission_classes = [IsAuthenticated, CanCreateListing]


class UpdateListingView(generics.UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingInputSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ListingsListView(generics.ListAPIView):
    queryset = Listing.objects.filter(is_active=True, active_confirmed_donation_conversation=None)
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class ListingsMeView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user)


class ListingsSpecificView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Listing.objects.all()


class ListingsBulkView(generics.GenericAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        listings = Listing.objects.filter(id__in=ids)
        serializer = self.get_serializer(listings, many=True)

        # map into dict with id as key
        listings_dict = {listing['id']: listing for listing in serializer.data}
        return Response(listings_dict, status=200)
