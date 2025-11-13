from rest_framework import serializers
from ..models import Listing
from ...users.api.serializers import LocationSerializer

from ...users.models import User, LocationCroatia


# Nested serializer for owner object: will produce { id, name, rating }
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ListingSerializer(serializers.ModelSerializer):
    # expose owner as an object with id, name and rating
    owner = OwnerSerializer(read_only=True)
    location = serializers.ReadOnlyField(source='location.cityName')

    class Meta:  # sta je class meta ???
        model = Listing  # model koji zelimo serijalizirati ili ti pretvoriti u json i natrag
        fields = ["id", "title", "content", "picture", "category", "condition", "location", "delivery",
                  "owner"]  # tocne podatke koje zelimo serijalizirati
        extra_kwargs = {"owner": {"read_only": True}}  # dopustamo da se otkrije vlasnik, ali se ne moze mijenjati


class LocationInputField(serializers.Field):
    def to_internal_value(self, data):
        try:
            location = LocationCroatia.objects.get(id=int(data))
            return location
        except LocationCroatia.DoesNotExist:
            raise serializers.ValidationError("Invalid location ID")

    def to_representation(self, value):
        return {
            "id": value.id,
            "cityName": value.cityName
        }


class ListingInputSerializer(serializers.ModelSerializer):
    location = LocationInputField()

    class Meta:
        model = Listing
        fields = ["title", "content", "picture", "condition", "category", "location", "delivery"]

    def create(self, validated_data):  # funkcija
        validated_data['owner'] = self.context['request'].user

        listing = Listing.objects.create(**validated_data)
        return listing

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.category = validated_data.get('category', instance.category)
        instance.location = validated_data.get('location', instance.location)
        instance.delivery = validated_data.get('delivery', instance.delivery)
        instance.save()
        return instance


class ListingSeeSerializer(serializers.ModelSerializer):
    # expose owner as nested object instead of separate fields
    owner = OwnerSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ["id", "title", "content", "picture", "condition", "category", "location", "delivery", "owner"]
        extra_kwargs = {"owner": {"read_only": True}}
