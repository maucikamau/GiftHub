from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from backend.users.models import User, LocationCroatia
from backend.campaigns.models import Campaign
import json


class CampaignTests(APITestCase):

    def setUp(self):
        """Set up test data."""
        # Create test users
        self.donor = User.objects.create_user(
            username='donor',
            email='donor@test.com',
            password='testpass123',
            role='donor'
        )
        self.recipient_association = User.objects.create_user(
            username='recipient',
            email='recipient@test.com',
            password='testpass123',
            role='recipient_association'
        )
        self.recipient = User.objects.create_user(
            username='other_recipient',
            email='other@test.com',
            password='testpass123',
            role='recipient'
        )

        # Create a location
        self.location = LocationCroatia.objects.get(cityName='Split')
        self.other_location = LocationCroatia.objects.get(cityName='Zagreb')

        # Create campaign
        self.campaign = Campaign.objects.create(
            title='School Supplies',
            description='Collecting school supplies for children in need.',
            location=self.location,
            wish_list=[
                {"name": "Notebook", "count": 50, "donated": 10},
                {"name": "Pen", "count": 100, "donated": 20},
            ],
            owner=self.recipient_association
        )

        self.client = APIClient()
        self.list_url = reverse('campaigns:allCampaigns')
        self.create_url = reverse('campaigns:createCampaign')
        self.me_url = reverse('campaigns:myCampaigns')
        self.detail_url = reverse('campaigns:pkCampaigns', kwargs={'pk': self.campaign.id})
        self.donate_url = reverse('campaigns:donateCampaign', kwargs={'item': 'Notebook'})

    def test_create_campaign_success(self):
        """Test successful campaign creation."""
        self.client.force_authenticate(user=self.recipient_association)

        data = {
            'title': 'Winter clothes',
            'description': 'Anything to keep warm this winter',
            'location': self.location.id,
            'wish_list': [{"name": "Jacket", "count": 10, "donated": 0}],
            'end_date': '2026-12-31T23:59:59Z'
        }

        # Obavezno format='json' zbog nested liste u wish_list
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.count(), 2)

        new_campaign = Campaign.objects.last()
        self.assertEqual(new_campaign.title, 'Winter clothes')
        self.assertEqual(new_campaign.owner, self.recipient_association)  # Provjera vlasnika iz request.user
        self.assertEqual(new_campaign.location, self.location)

    def test_create_campaign_unauthorized_user(self):
        """Test campaign failure for unauthorized user (not association)"""
        self.client.force_authenticate(user=self.recipient)

        data = {
            'title': 'Summer clothes',
            'description': 'This should fail',
            'location': self.location.id,
            'wish_list': [{"name": "Trunks", "count": 5, "donated": 0}],
            'end_date': '2026-12-31T23:59:59Z'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_campaign_invalid_location(self):
        """Test with non-existent location ID"""
        self.client.force_authenticate(user=self.recipient)
        data = {
            'title': 'Fail', 'description': '...',
            'location': 9999,
            'wish_list': []
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_campaign(self):
        """Test updating campaign's title and location"""
        self.client.force_authenticate(user=self.recipient_association)

        update_url = reverse('campaigns:updateCampaign', kwargs={'pk': self.campaign.id})

        data = {
            'title': 'Donations for kids',
            'location': self.other_location.id,
        }

        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.title, 'Donations for kids')
        self.assertEqual(self.campaign.location, self.other_location)

    def test_donor_can_see_campaigns(self):
        """Test that a donor can see the list of campaigns."""
        self.client.force_authenticate(user=self.donor)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_donate_success(self):
        """Test user can donate an item successfully."""
        self.client.force_authenticate(user=self.donor)

        # Doniramo 1 Bilježnicu (hardkodirano quantity=1 u view-u)
        data = {'campaign_id': self.campaign.id}

        response = self.client.post(self.donate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.wish_list[0]['donated'], 11)

    def test_donate_item_not_in_wishlist(self):
        """Test add item that is not in the wish list."""
        self.client.force_authenticate(user=self.donor)

        bad_url = reverse('campaigns:donateCampaign', kwargs={'item': 'Backpack'})
        data = {'campaign_id': self.campaign.id}

        response = self.client.post(bad_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
