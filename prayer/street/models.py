from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Userprofile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    longitude = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=12)
    latitude = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=12)
    accepted_terms_and_conditions = models.BooleanField(default=True)
    is_mobile_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='userprofilepics',default= 'userprofilepics/sank.png')
    allow_notification = models.IntegerField(default=1, help_text='0-OFF,1-ON', blank=True, null=True)
    rate_app = models.IntegerField(default=1, help_text='rate is from 1-5')
    is_admin = models.NullBooleanField()
    phone = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return '%s - %s'%(self.user.username, self.name)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(Userprofile, self).save(*args, **kwargs)


class PrayerRequest(models.Model):
    user = models.ForeignKey(Userprofile, blank=True, null=True)
    selected_date = models.DateTimeField(default=timezone.now)
    header = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Prayer Request"

    def __str__(self):
        return '%s - %s'%(self.user, self.header)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(PrayerRequest, self).save(*args, **kwargs)


class Like(models.Model):
    prayer_request = models.ForeignKey(PrayerRequest, blank=True, null=True)
    user = models.ForeignKey(Userprofile, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Like Prayer"

    def __str__(self):
        return unicode(self.prayer_request)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(Like, self).save(*args, **kwargs)


class Upcoming(models.Model):
    annoucement_des = models.TextField()
    annoucement_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Upcoming"

    def __str__(self):
        return (self.annoucement_des)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(Upcoming, self).save(*args, **kwargs)


class Langauage(models.Model):
    language_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Language'

    def __str__(self):
        return self.language_name

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(Langauage, self).save(*args, **kwargs)


class UserMedia(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    langauage = models.ForeignKey(Langauage, blank=True, null=True)
    video_link = models.URLField(blank=True)
    audio = models.FileField(upload_to='upload_to_audio', blank=True)
    video_image = models.ImageField(upload_to='uploadto_video_image', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'UserMedia'

    def __unicode__(self):
        return unicode(self.langauage)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(UserMedia, self).save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    like = models.ForeignKey(Like, blank=True, null=True)
    usermedia = models.ForeignKey(UserMedia, blank=True, null=True)
    notification_type = models.IntegerField(default=1, help_text='1-Like Added, 2-User Media Added')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Notification'

    def __str__(self):
        return self.notification_type

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(Notification, self).save(*args, **kwargs)


class About(models.Model):
    about_us = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'About'

    def __str__(self):
        return self.about_us

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(About, self).save(*args, **kwargs) 