from rest_framework import serializers

from backend.users.models import User, Association, LocationCroatia


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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCroatia
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:  # sta je class meta ???
        model = User  # model koji zelimo serijalizirati ili ti pretvoriti u json i natrag
        fields = ["id", "first_name", "last_name", "username", "email", "role", "location",
                  "registration_step", "chat_uid", "profile_image"]  # tocne podatke koje zelimo serijalizirati

    def create(self, validate_data):  # funkcija
        user = User.objects.create_user(**validate_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False, allow_null=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=LocationCroatia.objects.all(),
        source='location',
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "location", "location_id", "profile_image"]

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        
        if location_data:
            if isinstance(location_data, LocationCroatia):
                instance.location = location_data
            else:
                location = LocationCroatia.objects.get(**location_data)
                instance.location = location

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



