from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from backend.listings.api.serializers import ListingSerializer
from backend.listings.models import Listing


class CreateListView(generics.CreateAPIView):  # generičan view koji hendla kreiranje novog korisnika/objekta
    queryset = Listing.objects.all()  # pregledava da ne napravimo duplikata
    serializer_class = ListingSerializer  # javlja viewu koje podatke trebamo prihvatiti za novog korisnika
    permission_classes = [IsAuthenticated]  # tko smije ovo pozvati (u nasem slucaju svi mogu napraviti k


from django.shortcuts import render

# Create your views here.
