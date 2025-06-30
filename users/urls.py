from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),

]