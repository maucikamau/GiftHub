from rest_framework import serializers
from ..models import StripeConnectedAccount, Payment


class StripeConnectedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeConnectedAccount
        fields = [
            'id',
            'stripe_account_id',
            'charges_enabled',
            'payouts_enabled',
            'details_submitted',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'stripe_account_id',
            'charges_enabled',
            'payouts_enabled',
            'details_submitted',
            'created_at',
            'updated_at'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    donor_email = serializers.EmailField(source='donor.email', read_only=True)
    recipient_email = serializers.EmailField(source='recipient.email', read_only=True)
    campaign_title = serializers.CharField(source='campaign.title', read_only=True, allow_null=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True, allow_null=True)
    listing_id = serializers.IntegerField(source='listing.id', read_only=True, allow_null=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'donor',
            'donor_email',
            'recipient',
            'recipient_email',
            'listing',
            'listing_id',
            'listing_title',
            'campaign',
            'campaign_title',
            'stripe_payment_intent_id',
            'amount',
            'currency',
            'status',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'stripe_payment_intent_id',
            'status',
            'created_at',
            'updated_at'
        ]


class CreatePaymentIntentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.50)
    currency = serializers.CharField(max_length=3, default='eur')
    listing_id = serializers.IntegerField(required=True, help_text='ID of the listing being delivered')
    campaign_id = serializers.IntegerField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    metadata = serializers.JSONField(required=False, default=dict)


class AccountOnboardingSerializer(serializers.Serializer):
    refresh_url = serializers.URLField()
    return_url = serializers.URLField()

