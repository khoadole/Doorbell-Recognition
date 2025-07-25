from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-popup-template/', views.get_popup_template, name='get_popup_template'),
    path('history', views.history, name='history'),
    path('api/upload_frame', views.upload_frame, name='upload_frame'),
    path('api/view_feed', views.video_feed, name='video_feed'),
    path('api/latest-recognition', views.latest_recognition, name='latest_recognition'),
    path('api/open-door', views.open_door, name='open_door')
]