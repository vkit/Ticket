from street.constants import *
from street.serializers import *
# Sign up
def validate_signup(data):
	serializer = SignUpSerializer(data=data)
	if serializer.is_valid():
		return True, None
	else:
		return False, serializer.errors

def validate_login(data):
	serializer = LoginSerializer(data=data)
	if serializer.is_valid():
		return True, None
	else:
		return False, serializer.errors

def validate_prayer(data):
	serializer = AddPrayerSerializer(data=data)
	if serializer.is_valid():
		return True, None
	else:
		return False, serializer.errors

def validate_like(data):
	serializer = AddLikePrayerSerializer(data=data)
	if serializer.is_valid():
		return True, None
	else:
		return False, serializer.errors

def validate_userprofile(data):
	serializer = EditProfileSerializer(data=data)
	if serializer.is_valid():
		return True, None
	else:
		return False, serializer.errors

def validate_media(data):
	serializers = UploadMediaSerializer(data=data)
	if serializers.is_valid():
		return True, None
	else:
		return False, serializers.errors











