from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404

from backend.reviews.api.serializers import ReviewSerializer, ReviewListItemSerializer, OwnerSerializer
from backend.reviews.models import Review
from backend.users.models import User


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'perPage'
    max_page_size = 1000


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
                       'confirmed_donation_conversation') or not listing.confirmed_donation_conversation:
            return Response(
                {'error': 'Možete ostaviti recenziju samo za donacije koje su potvrđene.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Korisnik mora biti primatelj donacije
        if listing.confirmed_donation_conversation.recipient != request.user:
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
    serializer_class = ReviewListItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user_id = self.kwargs['user']
        return Review.objects.filter(donor__id=user_id).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs['user']
        donor = get_object_or_404(User, id=user_id)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            # Add donor info at the top level
            return Response({
                'donor': OwnerSerializer(donor).data,
                'reviews': paginated_response.data['results'],
                'count': paginated_response.data['count'],
                'next': paginated_response.data['next'],
                'previous': paginated_response.data['previous'],
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'donor': OwnerSerializer(donor).data,
            'reviews': serializer.data,
            'count': len(serializer.data),
            'next': None,
            'previous': None,
        })


class ReviewGetAvgView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user']
        stats = Review.objects.filter(donor__id=user_id).aggregate(
            average=Avg('rating'),
            total=Count('rating')
        )
        average_rating = stats['average'] or 0.0
        total = stats['total'] or 0
        stars = round(average_rating)
        return Response({'average': round(average_rating, 2), 'total': total, 'stars': stars}, status=status.HTTP_200_OK)
