from rest_framework import serializers
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from street.models import Userprofile
from .constants import *

# from street.code_msg import *

# from street.constants import *

# from street.utils import validate_phone_number, is_mobile_number_exist, is_email_exist
from django.core.exceptions import ValidationError

# Sign up 


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10, required=True)
    username = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(min_length=5, required=True)
    location = serializers.CharField(max_length=1000, required=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(min_length=5, required=True)


class AddPrayerSerializer(serializers.Serializer):
    selected_date = serializers.DateTimeField()
    header = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=1000, required=True)


class EditProfileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=15)
    street = serializers.CharField(max_length=1000)
    allow_notification = serializers.IntegerField()

    def validate_notification_status(self, allow_notification):
        if allow_notification not in [ON, OFF]:
            raise serializers.ValidationError({'allow_notification': codes_msg[1012]})
        return True



class AddLikePrayerSerializer(serializers.Serializer):
    prayer_id = serializers.IntegerField()


class UploadMediaSerializer(serializers.Serializer):
    langauage_id = serializers.IntegerField()
    video_link = serializers.URLField()
    audio = serializers.FileField()
    video_image = serializers.ImageField()

