from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('forgot_password', views.forgot_password, name = 'forgot_password'),
    path('reset_password', views.reset_password, name = 'reset_password'),
]