from django.contrib import admin

# Register your models here.
from .models import Userprofile, PrayerRequest, Like, Upcoming, Langauage, UserMedia, About
admin.site.register(Userprofile)
admin.site.register(PrayerRequest)
admin.site.register(Like)
admin.site.register(Upcoming)
admin.site.register(Langauage)
admin.site.register(UserMedia)
admin.site.register(About)