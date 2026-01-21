from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from backend.users.models import User, LocationCroatia
from backend.listings.models import Listing
from backend.reviews.models import Review
from backend.chat.models import ChatChannel


class ReviewsViewTests(APITestCase):

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
        self.location = LocationCroatia.objects.get(cityName='Osijek')

        # Create listings
        self.listingActive = Listing.objects.create(
            title='Test Listing 1',
            content='Test content 1',
            category='Electronics',
            condition='new',
            location=self.location,
            delivery='pickup',
            owner=self.donor,
            is_active=True
        )

        self.listingOver = Listing.objects.create(
            title='Test Listing 2',
            content='Test content 2',
            category='Books',
            condition='used',
            location=self.location,
            delivery='shipping',
            owner=self.donor,
            is_active=False
        )

        self.client = APIClient()
        self.create_url = reverse('reviews:createReview')
        self.list_url = reverse('reviews:listReviews', kwargs={'user': self.donor.id})
        self.avg_url = reverse('reviews:averageReviews', kwargs={'user': self.donor.id})

    def test_review_creation_requires_authentication(self):
        """Test that the endpoint requires authentication."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_list_requires_authentication(self):
        """Test that the endpoint requires authentication."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_review_success(self):
        """Test case for creating a review successfully."""
        self.client.force_authenticate(user=self.recipient)
        channel_id = f"{self.listingOver.id}-{self.recipient.chat_uid}"

        self.chat = ChatChannel.objects.create(
            listing=self.listingOver,
            donor=self.donor,
            recipient=self.recipient,
            stream_channel_id=channel_id
        )

        self.listingOver.confirmed_donation_conversation = self.chat
        self.listingOver.save()

        data = {
            'rating': 5,
            'comment': 'Great!',
            'for_listing': self.listingOver.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().rating, 5)

    def test_cannot_review_active_listing(self):
        """Test that reviewing an active listing is not allowed."""
        self.client.force_authenticate(user=self.recipient)

        data = {
            'rating': 3,
            'comment': 'Decent',
            'for_listing': self.listingActive.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('for_listing', response.data)

    def test_only_recipient_can_review(self):
        """Test that only the recipient can review the donation."""
        self.client.force_authenticate(user=self.donor)

        data = {
            'rating': 3,
            'comment': 'Decent',
            'for_listing': self.listingOver.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_review_twice(self):
        """Test that a user cannot review the same listing twice."""

        Review.objects.create(
            donor=self.donor,
            reviewer=self.recipient,
            for_listing=self.listingOver,
            rating=5,
            comment="First review"
        )

        self.client.force_authenticate(user=self.recipient)

        data = {
            'rating': 1,
            'for_listing': self.listingOver.id,
            'comment': 'Second review attempt'
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Review.objects.count(), 1)

    def test_get_average_rating(self):
            """Test average rating calculation for a donor with reviews."""
            # Create two reviews for the donor
            listingOver2 = Listing.objects.create(title='Drugi', owner=self.donor, is_active=False)

            Review.objects.create(donor=self.donor, reviewer=self.recipient, for_listing=self.listingOver, rating=5)
            Review.objects.create(donor=self.donor, reviewer=self.recipient, for_listing=listingOver2, rating=3)

            self.client.force_authenticate(user=self.recipient)
            response = self.client.get(self.avg_url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['average'], 4.0)

    def test_get_average_rating_no_reviews(self):
            """Test average for no reviews returns 0.0."""
            self.client.force_authenticate(user=self.recipient)

            response = self.client.get(self.avg_url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['average'], 0.0)

