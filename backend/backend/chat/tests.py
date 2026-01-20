from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch, MagicMock
from backend.users.models import User, LocationCroatia
from backend.listings.models import Listing
from backend.chat.models import ChatChannel


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
        self.location = LocationCroatia.objects.get(cityName='Rijeka')

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

        self.client = APIClient()
        self.token_url = reverse('chat:createStreamToken')
        self.delivery_req_url = reverse('chat:createRequest', kwargs={'listing_id': self.listing1.id})


    # Ovaj view zove StreamChat direktno, pa patchamo u VIEWS
    @patch('backend.chat.views.StreamChat')
    def test_create_stream_token(self, MockStreamChat):
        """Test creating a Stream token."""
        self.client.force_authenticate(user=self.recipient)

        # Mock setup
        mock_instance = MockStreamChat.return_value
        mock_instance.create_token.return_value = "fake_token_123"

        response = self.client.post(self.token_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], "fake_token_123")

    @patch('backend.chat.utils.StreamChat')
    def test_create_chat_channel(self, MockStreamChatUtils):
        """Test creating a chat channel."""
        self.client.force_authenticate(user=self.recipient)

        # Mock setup za utils
        mock_client = MockStreamChatUtils.return_value
        mock_channel = MagicMock()
        mock_client.channel.return_value = mock_channel

        self.create_chat_url = reverse('chat:createChatChannel', kwargs={'listing_id': self.listing1.id})
        response = self.client.post(self.create_chat_url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Provjerimo je li utils pozvao channel.create()
        mock_client.channel.assert_called()
        mock_channel.create.assert_called()

        # Provjera baze
        self.assertTrue(ChatChannel.objects.exists())
        channel = ChatChannel.objects.first()
        self.assertEqual(channel.listing, self.listing1)

    def test_create_delivery_request_invalid_listing(self):
        """Test creating a delivery request with an invalid listing ID."""
        self.client.force_authenticate(user=self.recipient)

        invalid_delivery_req_url = reverse('chat:createRequest', kwargs={'listing_id': 9999})
        data = {'delivery_type': 'shipping'}
        response = self.client.post(invalid_delivery_req_url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Oglas ne postoji.")

    @patch('backend.chat.views.StreamChat')
    @patch('backend.chat.utils.StreamChat')  # Moramo patchati i utils jer ga view poziva!
    def test_create_delivery_request(self, MockStreamUtils, MockStreamView):
        self.client.force_authenticate(user=self.recipient)

        # Mock setup (za View)
        mock_view_client = MockStreamView.return_value
        mock_view_channel = MagicMock()
        mock_view_client.channel.return_value = mock_view_channel
        mock_view_channel.send_message.return_value = {'message': {'id': 'msg-fake-999'}}

        # Mock setup (za Utils - samo da ne pukne kod kreiranja kanala)
        mock_utils_client = MockStreamUtils.return_value
        mock_utils_channel = MagicMock()
        mock_utils_client.channel.return_value = mock_utils_channel

        data = {'delivery_type': 'shipping'}
        response = self.client.post(self.delivery_req_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        channel = ChatChannel.objects.get(listing=self.listing1)
        self.assertEqual(channel.delivery_request_msg_id, 'msg-fake-999')

    def test_create_delivery_request_already_sent(self):
        """Test creating a delivery request when one has already been sent."""
        self.client.force_authenticate(user=self.recipient)
        channel_id = f"{self.listing1.id}-{self.recipient.chat_uid}"

        # Prvo kreiramo zahtjev za dostavu
        self.chat = ChatChannel.objects.create(
            stream_channel_id=channel_id,
            listing=self.listing1,
            donor=self.donor,
            recipient=self.recipient,
            delivery_check=True
        )

        self.listing1.active_confirmed_donation_conversation = self.chat
        self.listing1.save()


        data = {'delivery_type': 'shipping'}
        response = self.client.post(self.delivery_req_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('backend.chat.views.StreamChat')
    def test_accept_delivery_request(self, MockStreamChat):
        self.client.force_authenticate(user=self.donor)

        msg_id = "msg-123-abc"
        # Ručno kreiramo kanal da izbjegnemo utils logiku
        chat = ChatChannel.objects.create(
            stream_channel_id="test_channel",
            listing=self.listing2,
            donor=self.donor,
            recipient=self.recipient,
            delivery_check=True,
            delivery_request_msg_id=msg_id,
            delivery_type="shipping"
        )

        respond_url = reverse('chat:respondRequest', kwargs={'msg_id': msg_id})
        data = {'check': True}

        response = self.client.post(respond_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        chat.refresh_from_db()
        self.assertTrue(chat.delivery_accepted)

    # Odbijanje zahtjeva za dostavu
    @patch('backend.chat.views.StreamChat')
    def test_decline_delivery_request(self, MockStreamChat):
        self.client.force_authenticate(user=self.donor)

        msg_id = "msg-456-def"
        # Ručno kreiramo kanal da izbjegnemo utils logiku
        chat = ChatChannel.objects.create(
            stream_channel_id="test_channel_2",
            listing=self.listing2,
            donor=self.donor,
            recipient=self.other_recipient,
            delivery_check=True,
            delivery_request_msg_id=msg_id,
            delivery_type="pickup"
        )

        respond_url = reverse('chat:respondRequest', kwargs={'msg_id': msg_id})
        data = {'check': False}

        response = self.client.post(respond_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        chat.refresh_from_db()
        self.assertFalse(chat.delivery_accepted)
        self.assertFalse(chat.delivery_check)
        self.assertIsNone(chat.delivery_request_msg_id)
        self.assertIsNone(chat.delivery_type)

    # testiranje edge case: nepostojeći msg_id
    @patch('backend.chat.views.StreamChat')
    def test_respond_delivery_request_invalid_msg_id(self, MockStreamChat):
        self.client.force_authenticate(user=self.donor)

        invalid_msg_id = "nonexistent-msg-id"
        respond_url = reverse('chat:respondRequest', kwargs={'msg_id': invalid_msg_id})
        data = {'check': True}

        response = self.client.post(respond_url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
