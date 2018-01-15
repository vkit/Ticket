from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from datetime import date
from django.utils import timezone

# from datetime import datetime
from .models import Userprofile, PrayerRequest, Like, Upcoming, UserMedia, Notification, About, Langauage
from datetime import timedelta
from .constants import *
import base64
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .utils import check_availibity
from .validators import *
from .responsers import *


class Register(APIView):
    def post(self, request):
        try:
            data = request.POST
            valid, msg = validate_signup(data=data)
            if not valid:
                return fail_response(error_code=2044, data=msg)
            name = data.get('name')
            password = base64.b64decode(data.get('password'))
            username = data.get('username')
            location = data.get('location')
            availability = check_availibity(username=username)
            if availability:
                return fail_response(error_code=1013)

            user = User.objects.create_user(username=username, password=password)

            userprofile = Userprofile.objects.create(user=user, name=name, location=location)

            token, created = Token.objects.get_or_create(user=user)
            lis = list()
            if token:
                data = {'user_id':user.id,'username':username,'token':token.pk,'name':name, 'street': location}
                lis.append(data)
            return success_response(data={"registration_detail": lis})
        except Exception as e:
            print e


class Login(APIView):
    def post(self, request):
        try:
            data = request.POST
            valid, msg = validate_login(data=data)
            if not valid:
                return fail_response(error_code=2044, data=msg)
            username = data.get('username')
            password = base64.b64decode(data.get('password'))
            lis = list()
            availability = check_availibity(username=username)
            if not availability:
                return fail_response(error_code=1011)
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                user_detail = {
                    'token': token.pk,
                    'user': user.username,
                    'user_id': user.id
                }
                lis.append(user_detail)
                return success_response(data={"login_detail": lis})
        except Exception as e:
            print e


class PrayerRequestDetail(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            user = request.user
            data = request.POST
            userprofile = Userprofile.objects.get(user=user)
            valid, msg = validate_prayer(data=data)
            if not valid:
                return fail_response(error_code=2044, data=msg)
            PrayerRequest.objects.create(
                selected_date=data.get('selected_date'),
                header=data.get('header'),
                description=data.get('description'),
                user=userprofile
            )
            return success_response(code=9000)
        except Exception as e:
            print e

    def get(self, request):
            try:
                prayer_lists = PrayerRequest.objects.filter(is_active=True)
                lis = []
                for prayer_list in prayer_lists:
                    data = {
                        'prayer_id': prayer_list.id,
                        'header': prayer_list.header,
                        'user_id': prayer_list.user.user.id,
                        'description': prayer_list.description,
                        'created_at': prayer_list.created_at,
                        'user_name': prayer_list.user.name,
                        'posted_on': prayer_list.created_at,
                        'like_count': Like.objects.filter(prayer_request=prayer_list).count()
                    }
                    lis.append(data)
                return success_response(data={'prayer_list': lis})
            except Exception as e:
                print e

    def delete(self, request, prayer_id):
        user = request.user
        try:
            userprofile = Userprofile.objects.get(user=user)
            prayerrequest = PrayerRequest.objects.filter(pk=prayer_id, user=userprofile)
            if prayerrequest.exists():
                prayerrequest.delete()
                return success_response(code=9001)
            else:
                return fail_response(error_code=1008)
        except Exception as e:
            print e


class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    
    def put(self, request):
        try:
            user = request.user
            data = request.POST
            valid, msg = validate_userprofile(data=data)
            if not valid:
                return fail_response(error_code=2044, data=msg)
            userprofile = Userprofile.objects.get(user=user)
            userprofile.name = data.get('name')
            userprofile.location = data.get('street')
            userprofile.allow_notification = data.get('allow_notification')
            userprofile.save()
            return success_response(code=9002)
        except Exception as e:
            print e

    def get(self, request):
        try:
            user = request.user
            data = request.POST
            lis = []
            userprofile = Userprofile.objects.get(user=user)
            data = {
                'name': userprofile.name,
                'street': userprofile.location,
                'notification': userprofile.allow_notification,
                'avatar': userprofile.avatar.url if userprofile.avatar else ''
            }
            lis.append(data)
            return success_response(data={"user_profile_list": lis})
        except Exception as e:
            print e


class LikePrayer(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            user = request.user
            data = request.POST
            valid, msg = validate_like(data=data)
            if not valid:
                return fail_response(error_code=2044, data=msg)
            userprofile = Userprofile.objects.get(user=user)
            prayer_id = PrayerRequest.objects.get(id=data.get('prayer_id'))
            print prayer_id.user

            if Like.objects.filter(prayer_request=prayer_id,user=userprofile).exists():
                return fail_response(error_code=1014)
    
            Like.objects.create(
                prayer_request=prayer_id,
                user=userprofile
            )
            return success_response(code=9003)
        except Exception as e:
            print e


class UpcomingList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            upcoming_dates = Upcoming.objects.filter(annoucement_date__gte=timezone.now())
            lis = []
            for upcoming_date in upcoming_dates:
                data = {
                    'annoucement_id': upcoming_date.id,
                    'annoucement_description': upcoming_date.annoucement_des,
                    'annoucement_date': upcoming_date.annoucement_date,
                }
                lis.append(data)
            recenet_dates = Upcoming.objects.filter(annoucement_date__lt=timezone.now())
            lis1 = []
            for recenet_date in recenet_dates:
                data = {
                    'announcement_id': recenet_date.id,
                    'annoucement_description': recenet_date.annoucement_des,
                    'annoucement_date': recenet_date.annoucement_date,
                }
                lis1.append(data)
            return success_response(data={'upcoming_annoucement_count': upcoming_dates.count(),'upcoming_list': lis,'recent_list': lis1})
        except Exception as e:
            print e


class ResourceList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            usermedias = UserMedia.objects.filter(is_active=True)
            lis = []
            for usermedia in usermedias:
                data = {
                    'resource_id': usermedia.id,
                    'langauage_id': usermedia.langauage.id,
                    'video_url': usermedia.video_link,
                    'audio': usermedia.audio.url if usermedia.audio else '',
                    'video_image': usermedia.video_image.url if usermedia.video_image else '',
                    'user_id': usermedia.user.id,
                    'user_name': usermedia.user.username
                }
                lis.append(data)
            return success_response(data={"resource_list": lis})
        except Exception as e:
            print e


class AboutList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            about = About.objects.values('about_us').filter(is_active=True)
            if about.count > 0:
                about.first
            else:
                about = dict()
            return success_response(data=about)
        except Exception as e:
            print e


class PrayerYesturdayList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            usermedias = UserMedia.objects.filter(created_at__lte=timezone.now()-timedelta(days=1))
            lis = []
            for usermedia in usermedias:
                data = {
                    'resource_id': usermedia.id,
                    'langauage_id': usermedia.langauage.id,
                    'video_url': usermedia.video_link,
                    'audio': usermedia.audio.url if usermedia.audio else '',
                    'video_image': usermedia.video_image.url if usermedia.video_image else '',
                    'user_id': usermedia.user.id,
                    'user_name': usermedia.user.username
                }
                lis.append(data)
            return success_response(data={"resource_list": lis})
        except Exception as e:
            print e


class TodayList(APIView):
    def get(self, request):
        try:
            today = date.today()

            usermedias = UserMedia.objects.filter(created_at__day=today.day)
            lis = []
            for usermedia in usermedias:
                data = {
                    'resource_id': usermedia.id,
                    'langauage_id': usermedia.langauage.id,
                    'video_url': usermedia.video_link,
                    'audio': usermedia.audio.url if usermedia.audio else '',
                    'video_image': usermedia.video_image.url if usermedia.video_image else '',
                    'user_id': usermedia.user.id,
                    'user_name': usermedia.user.username
                }
                lis.append(data)
            return success_response(data={"resource_list": lis})
        except Exception as e:
            print e


class PrayerSevendayList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            usermedias = UserMedia.objects.filter(created_at__lte=timezone.now()-timedelta(days=7))
            lis = []
            for usermedia in usermedias:
                data = {
                    'resource_id': usermedia.id,
                    'langauage_id': usermedia.langauage.id,
                    'video_url': usermedia.video_link,
                    'audio': usermedia.audio.url if usermedia.audio else '',
                    'video_image': usermedia.video_image.url if usermedia.video_image else '',
                    'user_id': usermedia.user.id,
                    'user_name': usermedia.user.username
                }
                lis.append(data)
            return success_response(data={"resource_list": lis})
        except Exception as e:
            print e


class UploadMedia(APIView):
    def post(self, request):
        try:
            user = request.user
            data = request.POST
            profile = Userprofile.objects.get(user=user)
            if profile.is_admin:
                UserMedia.objects.create(
                    user=user,
                    langauage=Langauage.objects.get(id=data.get('langauage_id')),
                    video_link=data.get('video_link'),
                    audio=data.get('audio'),
                    video_image=data.get('video_image')

                )
                return success_response(code=1020)
            else:
                return fail_response(error_code=1018)
        except Exception as e:
            print e

# class UserActivity(APIView):
#     def get(self, request):
#         try:
#             user_notifications = Notification.objects.filter(
#                 Q(is_active=True)
#                 &
#                 Q(
#                     Q(notification_type=USER_NOTIFICATION_LIKED)
#                     |
#                     Q(notification_type=USER_NOTIFICATION_MEDIA_ADDED))
#                 )
#             notification_list = list()
#             for user_notification in user_notifications:
#                 activity_message = ''
