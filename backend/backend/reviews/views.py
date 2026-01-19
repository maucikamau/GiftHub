from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg

from backend.reviews.api.serializers import ReviewSerializer
from backend.reviews.models import Review


class ReviewSetView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        listing = serializer.validated_data.get('for_listing')

        # Provjeri je li oglas neaktivan
        if listing.is_active:
            return Response(
                {
                    'error': 'Ne možete ostaviti recenziju za aktivan oglas. Recenzije se mogu ostaviti samo nakon što je donacija završena.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Provjeri postoji li potvrđena donacija za oglas
        if not hasattr(listing,
                       'active_confirmed_donation_conversation') or not listing.active_confirmed_donation_conversation:
            return Response(
                {'error': 'Možete ostaviti recenziju samo za donacije koje su potvrđene.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Korisnik mora biti primatelj donacije
        if listing.active_confirmed_donation_conversation.recipient != request.user:
            return Response(
                {'error': 'Možete ostaviti recenziju samo za donacije koje ste primili.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Provjeri je li korisnik već ostavio recenziju za ovaj oglas
        donor = listing.owner
        if Review.objects.filter(reviewer=request.user, for_listing=listing).exists():
            return Response(
                {'error': 'Već ste ostavili recenziju za ovu donaciju.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(reviewer=request.user, donor=donor)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewSeeListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user']
        return Review.objects.filter(donor__id=user_id)


class ReviewGetAvgView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user']
        average_rating = Review.objects.filter(donor__id=user_id).aggregate(average=Avg('rating'))['average']
        if average_rating is None:
            average_rating = 0.0
        return Response({'average_rating': round(average_rating, 2)}, status=status.HTTP_200_OK)
