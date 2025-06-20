from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-popup-template/', views.get_popup_template, name='get_popup_template'),
    path('history', views.history, name='history'),
    path('profile', views.profile, name='profile'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
]