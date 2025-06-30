from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-popup-template/', views.get_popup_template, name='get_popup_template'),
    path('history', views.history, name='history'),

]