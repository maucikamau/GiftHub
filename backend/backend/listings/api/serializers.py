from rest_framework import serializers
from backend.listings.models import Listing

class ListingSerializer(serializers.ModelSerializer):
    class Meta: #sta je class meta ???
        model = Listing #model koji zelimo serijalizirati ili ti pretvoriti u json i natrag
        fields = ["id", "title", "content", "picture", "category", "status", "location", "delivery", "owner"] #tocne podatke koje zelimo serijalizirati
        extra_kwargs = {"owner": {"read_only": True}} #dopustamo da se otkrije vlasnik, ali se ne moze mijenjati

    def create(self, validate_data): #funkcija
        validate_data['owner'] = self.context['request'].user
        listing = Listing.objects.create(**validate_data) #ako su dobro pokriveni podatci iz fields validirana su preko "modelseliazer"
            #  znaci da se podijele podatci i tako ih proslijedimo iz bibiloteke
        return listing #funkcija koja se zove kad zelimo napraviti nove verziju korisnika
