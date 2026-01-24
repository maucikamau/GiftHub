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

class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserUdrugaAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = ["association_name", "association_email"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCroatia
        fields = "__all__"


class OrganizationUserSerializer(serializers.ModelSerializer):
    association_name = serializers.CharField(source='organization.association_name')
    association_email = serializers.EmailField(source='organization.association_email')
    location = LocationSerializer()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "role", "location",
                  "registration_step", "chat_uid", "profile_image", "association_name", "association_email"]


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
    association_name = serializers.CharField(required=False, allow_blank=True)
    association_email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "location", "location_id", "profile_image", "association_name", "association_email"]

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        association_name = validated_data.pop('association_name', None)
        association_email = validated_data.pop('association_email', None)

        if location_data:
            if isinstance(location_data, LocationCroatia):
                instance.location = location_data
            else:
                location = LocationCroatia.objects.get(**location_data)
                instance.location = location

        if instance.role == 'recipient_association':
             try:
                 org = instance.organization
                 if association_name is not None:
                     org.association_name = association_name
                 if association_email is not None:
                     org.association_email = association_email
                 org.save()
             except Association.DoesNotExist:
                 pass

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



