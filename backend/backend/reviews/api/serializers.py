from rest_framework import serializers
from backend.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "donor", "reviewer", "rating", "comment", "created_at"]
        read_only_fields = ["id", "created_at"]
