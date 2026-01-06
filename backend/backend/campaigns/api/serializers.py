from rest_framework import serializers
from ..models import Campaign
from ...users.api.serializers import LocationSerializer
from ...users.models import User, LocationCroatia


# Nested serializer for owner object: will produce { id, name, rating }
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CampaignSerializer(serializers.ModelSerializer):
    # expose owner as an object with id, name and rating
    owner = OwnerSerializer(read_only=True)
    location = serializers.ReadOnlyField(source='location.cityName')

    class Meta:  # sta je class meta ???
        model = Campaign  # model koji zelimo serijalizirati ili ti pretvoriti u json i natrag
        fields = ["id", "title", "content", "picture", "description", "location", "wish_list",
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


class CampaignInputSerializer(serializers.ModelSerializer):
    location = LocationInputField()

    class Meta:
        model = Campaign
        fields = ["id", "title", "content", "picture", "description", "location", "wish_list"]

    def create(self, validated_data):  # funkcija
        validated_data['owner'] = self.context['request'].user

        campaign = Campaign.objects.create(**validated_data)
        return campaign

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.condition = validated_data.get('description', instance.condition)
        instance.location = validated_data.get('location', instance.location)
        instance.delivery = validated_data.get('wish_list', instance.delivery)
        instance.save()
        return instance


class CampaignSeeSerializer(serializers.ModelSerializer):
    # expose owner as nested object instead of separate fields
    owner = OwnerSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = ["id", "title", "content", "picture", "description", "location", "wish_list",
                  "owner"]
        extra_kwargs = {"owner": {"read_only": True}}
