from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from backend.listings.models import Listing
from backend.chat.models import ChatChannel
from backend.users.models import User, LocationCroatia


class ActiveDonationsViewTests(APITestCase):

    def setUp(self):
        """Set up test data."""
        # Create test users
        self.donor = User.objects.create_user(
            username='donor',
            email='donor@test.com',
            password='testpass123',
            role='donor'
        )
        self.recipient = User.objects.create_user(
            username='recipient',
            email='recipient@test.com',
            password='testpass123',
            role='recipient'
        )
        self.other_recipient = User.objects.create_user(
            username='other_recipient',
            email='other@test.com',
            password='testpass123',
            role='recipient'
        )

        # Create a location
        self.location = LocationCroatia.objects.get(cityName='Zagreb')

        # Create listings
        self.listing1 = Listing.objects.create(
            title='Test Listing 1',
            content='Test content 1',
            category='Electronics',
            condition='new',
            location=self.location,
            delivery='pickup',
            owner=self.donor,
            is_active=True
        )

        self.listing2 = Listing.objects.create(
            title='Test Listing 2',
            content='Test content 2',
            category='Books',
            condition='used',
            location=self.location,
            delivery='shipping',
            owner=self.donor,
            is_active=True
        )

        self.listing3 = Listing.objects.create(
            title='Test Listing 3',
            content='Test content 3',
            category='Clothes',
            condition='new',
            location=self.location,
            delivery='pickup',
            owner=self.donor,
            is_active=True
        )

        # Create chat channels
        self.chat1 = ChatChannel.objects.create(
            stream_channel_id='channel1',
            listing=self.listing1,
            donor=self.donor,
            recipient=self.recipient,
            delivery_check=True,
            delivery_accepted=True
        )

        self.chat2 = ChatChannel.objects.create(
            stream_channel_id='channel2',
            listing=self.listing2,
            donor=self.donor,
            recipient=self.other_recipient,
            delivery_check=True,
            delivery_accepted=True
        )

        # Set active confirmed donation conversations
        self.listing1.confirmed_donation_conversation = self.chat1
        self.listing1.save()

        self.listing2.confirmed_donation_conversation = self.chat2
        self.listing2.save()

        self.client = APIClient()
        self.url = reverse('listings:activeDonations')

    def test_active_donations_requires_authentication(self):
        """Test that the endpoint requires authentication."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recipient_sees_own_active_donations(self):
        """Test that recipient sees only their active donations."""
        self.client.force_authenticate(user=self.recipient)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.listing1.id)
        self.assertEqual(response.data['results'][0]['title'], 'Test Listing 1')

    def test_other_recipient_sees_own_active_donations(self):
        """Test that a different recipient sees their own donations."""
        self.client.force_authenticate(user=self.other_recipient)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.listing2.id)

    def test_donor_sees_no_active_donations(self):
        """Test that donors don't see listings as active donations."""
        self.client.force_authenticate(user=self.donor)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_inactive_listing_not_shown(self):
        """Test that inactive listings are not shown in active donations."""
        # Mark listing as inactive
        self.listing1.is_active = False
        self.listing1.save()

        self.client.force_authenticate(user=self.recipient)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_listing_without_confirmed_conversation_not_shown(self):
        """Test that listings without confirmed conversations are not shown."""
        # Remove the active confirmed donation conversation
        self.listing1.confirmed_donation_conversation = None
        self.listing1.save()

        self.client.force_authenticate(user=self.recipient)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_response_includes_owner_details(self):
        """Test that response includes owner details."""
        self.client.force_authenticate(user=self.recipient)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data['results'][0]
        self.assertIn('owner', result)
        self.assertEqual(result['owner']['username'], 'donor')

    def test_response_includes_location_details(self):
        """Test that response includes location details."""
        self.client.force_authenticate(user=self.recipient)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data['results'][0]
        self.assertIn('location', result)
        self.assertEqual(result['location']['cityName'], 'Zagreb')

