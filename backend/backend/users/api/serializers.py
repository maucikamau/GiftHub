from rest_framework import serializers

from backend.users.models import User, Association

class UserSerializer(serializers.ModelSerializer):
    class Meta:  # sta je class meta ???
        model = User  # model koji zelimo serijalizirati ili ti pretvoriti u json i natrag
        fields = ["id", "first_name", "last_name", "username", "email", "role", "location",
                  "registration_step"]  # tocne podatke koje zelimo serijalizirati

    def create(self, validate_data):  # funkcija
        user = User.objects.create_user(**validate_data)
        return user


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]

class UserBasicInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "location"]


class UserUdrugaAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = ["association_name", "association_email"]


class OrganizationUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

