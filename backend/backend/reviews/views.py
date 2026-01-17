from django.shortcuts import render
from rest_framework import generics

from backend.reviews.api.serializers import ReviewSerializer
from backend.reviews.models import Review


# Create your views here.
class ReviewSetView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
