from rest_framework import serializers
from ..models import Listing

from ...users.models import User


# Nested serializer for owner object: will produce { id, name, rating }
class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]

class ListingSerializer(serializers.ModelSerializer):
    # expose owner as an object with id, name and rating
    owner = OwnerSerializer(read_only=True)

    class Meta: #sta je class meta ???
        model = Listing #model koji zelimo serijalizirati ili ti pretvoriti u json i natrag
        fields = ["id", "title", "content", "picture", "category", "condition", "location", "delivery", "owner"] #tocne podatke koje zelimo serijalizirati
        extra_kwargs = {"owner": {"read_only": True}} #dopustamo da se otkrije vlasnik, ali se ne moze mijenjati

    def create(self, validated_data): #funkcija
        validated_data['owner'] = self.context['request'].user
        listing = Listing.objects.create(**validated_data) #ako su dobro pokriveni podatci iz fields validirana su preko "modelseliazer"
            #  znaci da se podijele podatci i tako ih proslijedimo iz bibiloteke
        return listing #funkcija koja se zove kad zelimo napraviti nove verziju korisnika

class ListingSeeSerializer(serializers.ModelSerializer):
    # expose owner as nested object instead of separate fields
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ["id", "title", "content", "picture", "condition", "category", "location", "delivery", "owner"]
        extra_kwargs = {"owner": {"read_only": True}}
