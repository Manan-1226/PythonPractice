from rest_framework import serializers
from core.models import User, UserProfile


class UserLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=30)

    def validate(self, data):
        return data


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "UID",
            "username",
            "phone_number",
            "country_code",
            "is_active",
            "last_login",
        )
        read_only_fields = ("UID",)


class UserProfileInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "email")
        read_only_fields = ()
