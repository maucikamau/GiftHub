from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from backend.campaigns.api.serializers import CampaignSerializer, CampaignInputSerializer
from backend.campaigns.models import Campaign
#from backend.campaigns.permissions import IsOwnerOrReadOnly, CanCreateListing


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'perPage'
    max_page_size = 1000


class CreateCampaignView(generics.CreateAPIView):
    queryset = Campaign.objects.all()  # pregledava da ne napravimo duplikata
    serializer_class = CampaignInputSerializer  # javlja viewu koje podatke trebamo prihvatiti za novog korisnika
    permission_classes = [IsAuthenticated] #dodati isto kao CanCreateListing


class UpdateCampaignView(generics.UpdateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignInputSerializer
    permission_classes = [IsAuthenticated] #dodati isto kao IsOwnerOrReadOnly


class CampaignListView(generics.ListAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class CampaignsMeView(generics.ListAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)


class CampaignSpecificView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated] #dodati isto kao IsOwnerOrReadOnly kopiju
    queryset = Campaign.objects.all()


class CampaignDonate(generics.CreateAPIView):
    pass
