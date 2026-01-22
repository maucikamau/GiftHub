from rest_framework import generics, status
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
    queryset = Listing.objects.filter(is_active=True, confirmed_donation_conversation=None)
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort_by', None)
        location = self.request.query_params.get('location', None)

        if location:
            queryset = queryset.filter(location__id=location)

        if sort_by == "created_at_asc":
            queryset = queryset.order_by('-created_at')

        elif sort_by == "created_at_desc":
            queryset = queryset.order_by('created_at')

        return queryset.select_related('owner', 'location')


class ListingsMeView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user)


class ListingsSpecificView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Listing.objects.all()

    def get(self, request, *args, **kwargs):
        listing = self.get_object()

        data = self.get_serializer(listing).data

        # if the listing has a confirmed donation conversation,
        # and another user is trying to fetch the listing
        # deny it because it is no longer available.
        if (listing.confirmed_donation_conversation and
            listing.confirmed_donation_conversation.recipient.id != request.user.id and
            listing.owner.id != request.user.id):
            return Response({'detail': 'Ovaj oglas više nije dostupan'}, status=status.HTTP_403_FORBIDDEN)

        if listing.confirmed_donation_conversation:
            data['conversation_id'] = listing.confirmed_donation_conversation.stream_channel_id

        return Response(data)


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


class ActiveDonationsView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user

        return Listing.objects.filter(
            is_active=True,
            confirmed_donation_conversation__isnull=False,
            confirmed_donation_conversation__recipient=user
        ).select_related('owner', 'location', 'confirmed_donation_conversation')


class ConfirmDeliveryView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        from django.shortcuts import get_object_or_404

        listing = get_object_or_404(Listing, pk=pk)
        user = request.user

        # Provjeri da postoji potvrđena donacija za ovaj oglas
        if not listing.confirmed_donation_conversation:
            return Response(
                {'error': 'Donacija nije potvrđena za ovaj oglas'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Provjeri da li je trenutni korisnik primatelj donacije
        if listing.confirmed_donation_conversation.recipient != user:
            return Response(
                {'error': 'Nemate dozvolu potvrditi primopredaju za ovaj oglas'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Deactivate the listing
        listing.is_active = False
        listing.status = 'completed'
        listing.save()

        return Response(
            {'message': 'Potvrda primopredaje uspješna'},
            status=status.HTTP_200_OK
        )
