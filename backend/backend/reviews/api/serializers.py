from rest_framework import serializers
from backend.reviews.models import Review
from backend.listings.models import Listing
from backend.listings.api.serializers import ListingSerializer


class ReviewSerializer(serializers.ModelSerializer):
    for_listing = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.filter(is_active=False),
        write_only=True,
        required=True
    )
    listing = ListingSerializer(source='for_listing', read_only=True)

    class Meta:
        model = Review
        fields = ["id", "donor", "reviewer", "rating", "comment", "for_listing", "listing", "created_at"]
        read_only_fields = ["id", "created_at", "reviewer", "donor", "listing"]
        extra_kwargs = {
            'comment': {'required': False, 'allow_blank': True}
        }
