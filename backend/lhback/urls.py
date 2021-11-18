from django.urls import path

from . import views

urlpatterns = [
    path('announcements/list', views.AnnoucementList, name='announcements'),
    path('announcements/<int:announcement_id>/', views.AnnouncementDetail, name='announcementDetail'),
]
