from django.conf.urls import url, include

from street import views

urlpatterns = [
    url(r'^register/$', views.Register.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^add_prayer/$', views.PrayerRequestDetail.as_view()),
    url(r'^prayer_list/$', views.PrayerRequestDetail.as_view()),
    url(r'^delete_prayer/(?P<prayer_id>[0-9]+)/$',views.PrayerRequestDetail.as_view(),name='delete_prayer'),
    
    url(r'^like/$', views.LikePrayer.as_view()),
    url(r'^upcoming_list/$', views.UpcomingList.as_view()),
    # url(r'^recent_list/$', views.RecentList.as_view()),
    url(r'^edit_userprofile/$', views.UserProfile.as_view()),
    url(r'^userprofile_list/$', views.UserProfile.as_view()),
    url(r'^resource_list/$', views.ResourceList.as_view()),
    url(r'^about_list/$', views.AboutList.as_view()),
    url(r'^yesturday_list/$', views.PrayerYesturdayList.as_view()),
    url(r'^sevenday_list/$', views.PrayerSevendayList.as_view()),
    url(r'^today_list/$', views.TodayList.as_view()),
    url(r'^upload_media/$', views.UploadMedia.as_view()),

]