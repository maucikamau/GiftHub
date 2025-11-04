from rest_framework import serializers

from backend.users.models import User


'''class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }'''


class UserSerializer(serializers.ModelSerializer):
    class Meta: #sta je class meta ???
        model = User #model koji zelimo serijalizirati ili ti pretvoriti u json i natrag
        fields = ["id", "first_name", "last_name", "password", "email", "role", "location"] #tocne podatke koje zelimo serijalizirati
        extra_kwargs = {"password": {"write_only": True}} #prihvacamo sifre, ali ih ne vracamo

    def create(self, validate_data): #funkcija
        print("VALIDATED DATA:", validate_data)
        user = User.objects.create_user(**validate_data) #ako su dobro pokriveni podatci iz fields validirana su preko "modelseliazer"
            #  znaci da se podijele podatci i tako ih proslijedimo iz bibiloteke
        return user #funkcija koja se zove kad zelimo napraviti nove verziju korisnika


