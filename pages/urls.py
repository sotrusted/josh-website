from django.urls import path
from . import views

urlpatterns = [
    path('video/', views.video_list, name='video_list'),
    path('listen/', views.listen, name='listen'),
    # Flat pages — bio, services, lessons, sheet-music, orchestra, etc.
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]
