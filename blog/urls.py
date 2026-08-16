from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.post_list, {'category': 'news'}, name='news'),
    path('events/', views.post_list, {'category': 'events'}, name='events'),
    path('press/', views.post_list, {'category': 'press'}, name='press'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
]
