from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from backend.campaigns.api.serializers import CampaignSerializer, CampaignInputSerializer
from backend.campaigns.models import Campaign
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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


class CampaignDonate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item):
        # Get the campaign ID and quantity from request data
        campaign_id = request.data.get('campaign_id')
        quantity = 1 # Default

        if not campaign_id:
            return Response(
                {"error": "campaign_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            campaign = Campaign.objects.get(id=campaign_id)

            print(f"Campaign ID: {campaign_id}")
            print(f"Wish list before donation: {campaign.wish_list}")
            print(f"Item to donate: {item}")
            print(f"Quantity to donate: {quantity}")
        except Campaign.DoesNotExist:
            return Response(
                {"error": "Campaign not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Find the item in wish_list
        item_found = False
        for wish_item in campaign.wish_list:
            if wish_item.get('name') == item:
                item_found = True

                # Check if donation quantity is valid
                remaining = wish_item['count'] - wish_item['donated']
                if quantity > remaining:
                    return Response(
                        {
                            "error": f"Cannot donate {quantity}. Only {remaining} needed.",
                            "needed": wish_item['count'],
                            "already_donated": wish_item['donated'],
                            "remaining": remaining
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Update donated count
                wish_item['donated'] += quantity

                print(f"Item '{item}' updated: count={wish_item['count']}, donated={wish_item['donated']}")
                break

        if not item_found:
            return Response(
                {"error": "Item not found in campaign wish list"},
                status=status.HTTP_404_NOT_FOUND
            )

        campaign.save()

        print(f"Wish list after donation: {campaign.wish_list}")

        return Response(
            {
                "message": f"Successfully donated {quantity} {item}(s)",
                "wish_list": campaign.wish_list
            },
            status=status.HTTP_200_OK
        )
