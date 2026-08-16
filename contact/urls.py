from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('submit/', views.contact_submit, name='contact_submit'),
    path('subscribe/', views.mailing_list_subscribe, name='mailing_list_subscribe'),
]
