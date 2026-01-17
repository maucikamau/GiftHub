import stripe
from django.conf import settings
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from stream_chat import StreamChat

from ..models import StripeConnectedAccount, Payment
from .serializers import (
    StripeConnectedAccountSerializer,
    PaymentSerializer,
    CreatePaymentIntentSerializer,
    AccountOnboardingSerializer
)
from backend.listings.models import Listing
from ...chat.models import ChatChannel

# Initialize Stripe with API key from environment
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeConnectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing Stripe Connect accounts.
    Only donors can create connected accounts.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StripeConnectedAccountSerializer

    def get_queryset(self):
        return StripeConnectedAccount.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='link')
    def create_account(self, request):
        user = request.user

        if user.role != 'donor':
            return Response(
                {'error': 'Only donors can create connected accounts'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if user already has a connected account
        if hasattr(user, 'stripe_connected_account'):
            return Response(
                {'error': 'User already has a connected account'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create a Stripe Connect account
            account = stripe.Account.create(
                type='express',
                country='HR',  # Croatia
                email=user.email,
                capabilities={
                    'card_payments': {'requested': True},
                    'transfers': {'requested': True},
                },
                business_type='individual',
                business_profile={
                    "mcc": "4215",
                    "product_description": "Donation platform for delivery services"
                }
            )

            # Save the account to database
            connected_account = StripeConnectedAccount.objects.create(
                user=user,
                stripe_account_id=account.id
            )

            serializer = self.get_serializer(connected_account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='onboarding-link')
    def create_onboarding_link(self, request):
        """
        Create an onboarding link to redirect the donor to complete account setup.
        """
        user = request.user

        if user.role != 'donor':
            return Response(
                {'error': 'Only donors can access onboarding'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if user has a connected account
        if not hasattr(user, 'stripe_connected_account'):
            return Response(
                {'error': 'No connected account found. Please create one first.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AccountOnboardingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            account_id = user.stripe_connected_account.stripe_account_id

            # Create account link for onboarding
            account_link = stripe.AccountLink.create(
                account=account_id,
                refresh_url=serializer.validated_data['refresh_url'],
                return_url=serializer.validated_data['return_url'],
                type='account_onboarding',
            )

            return Response({
                'url': account_link.url,
                'expires_at': account_link.expires_at
            })

        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], url_path='account-status')
    def get_account_status(self, request):
        """
        Get the current status of the user's connected account.
        """
        user = request.user

        if not hasattr(user, 'stripe_connected_account'):
            return Response(
                {'error': 'No connected account found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            account_id = user.stripe_connected_account.stripe_account_id
            account = stripe.Account.retrieve(account_id)

            # Update local database with latest info
            connected_account = user.stripe_connected_account
            connected_account.charges_enabled = account.charges_enabled
            connected_account.payouts_enabled = account.payouts_enabled
            connected_account.details_submitted = account.details_submitted
            connected_account.save()

            # Grant payment permission if account is fully set up
            if connected_account.charges_enabled and connected_account.details_submitted:
                try:
                    permission = Permission.objects.get(
                        content_type__app_label='payments',
                        codename='view_payment'
                    )
                    if not user.user_permissions.filter(id=permission.id).exists():
                        user.user_permissions.add(permission)
                except Permission.DoesNotExist:
                    pass  # Permission will be created after migration

            serializer = self.get_serializer(connected_account)
            return Response(serializer.data)

        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing payments.
    Supports creating payment intents and viewing payment history.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        """Return payments where user is either donor or recipient."""
        user = self.request.user
        return Payment.objects.filter(
            Q(donor=user) | Q(recipient=user)
        )

    @action(detail=False, methods=['post'], url_path='create-payment-intent')
    def create_payment_intent(self, request):
        """
        Create a payment intent for a delivery payment.
        The donor creates the payment intent for the recipient to pay.
        The donor must have a connected Stripe account to receive the payment.
        """

        serializer = CreatePaymentIntentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        chat = get_object_or_404(ChatChannel, stream_channel_id=validated_data['chat_channel_id'])
        donor = chat.donor
        listing = chat.listing
        recipient = chat.recipient

        # Only the listing owner (donor) can create payment intents
        if request.user.chat_uid != donor.chat_uid:
            return Response(
                {'error': 'Only the listing owner can create payment intents for this listing'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not chat.delivery_check or not chat.delivery_accepted or chat.delivery_type != 'shipping':
            return Response(
                {'error': 'There is no accepted delivery request for this chat channel'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if donor has a connected account that is fully set up
        if not hasattr(donor, 'stripe_connected_account'):
            return Response(
                {'error': 'The donor has not set up their Stripe account yet'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not donor.stripe_connected_account.charges_enabled:
            return Response(
                {'error': 'The donor\'s Stripe account is not yet enabled for charges'},
                status=status.HTTP_400_BAD_REQUEST
            )


        # TODO: check that there's an active conversation between donor and recipient

        product = {
            'name': f'Dostava — {listing.title}',
            'description': f"Cijena troškova dostave za donaciju '{listing.title}' donatora {donor.get_full_name()}.",
        }

        try:
            # Convert amount to cents (Stripe uses cents)
            amount_cents = int(validated_data['amount'] * 100)

            # Create payment link
            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    'price_data': {
                        'currency': validated_data['currency'],
                        'product_data': product,
                        'unit_amount': amount_cents,
                    },
                    'quantity': 1,
                }],
                metadata={
                    'listing_id': str(listing.id),
                    'donor_id': str(donor.id),
                    'recipient_id': str(recipient.id),
                }
            )

            # Create payment record
            payment = Payment.objects.create(
                name=product['name'],
                donor=donor,
                recipient=recipient,
                listing=listing,
                stripe_payment_id=payment_link.id,
                pay_url=payment_link.url,
                amount=validated_data['amount'],
                currency=validated_data['currency'],
                description=product['description'],
                status='pending'
            )

            chat.payment = payment
            chat.save()

            # Send a message in the conversation thread
            chat_message = (
                f"Kreirana je uplata za troškove dostave u iznosu od "
                f"{validated_data['amount']} {validated_data['currency'].upper()}.\n"
                f"Molimo izvršite uplatu putem sljedećeg linka: {payment_link.url}"
            )
            client = StreamChat(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)
            channel = client.channel("messaging", chat.stream_channel_id)

            channel.send_message(
                {
                    "text": chat_message,
                    "type": "system",
                    "messageType": "PaymentRequest",
                    "payment_id": str(payment.id),
                    "stripe_payment_id": str(payment.stripe_payment_id),
                    "amount": float(payment.amount),
                    "payment_url": payment.pay_url,
                    "currency": payment.currency,
                },
                "gifthub"
            )

            return Response({
                'payment_id': payment.id,
                'url': payment_link.url,
                'stripe_payment_id': payment_link.id,
                'amount': float(payment.amount),
                'currency': payment.currency,
                'listing_id': listing.id,
                'donor_id': donor.id
            }, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], url_path='my-payments')
    def my_payments(self, request):
        payments = Payment.objects.filter(recipient=request.user).order_by('-created_at')
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='received-payments')
    def received_payments(self, request):
        payments = Payment.objects.filter(donor=request.user).order_by('-created_at')
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

