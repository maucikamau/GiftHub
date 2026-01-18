from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
