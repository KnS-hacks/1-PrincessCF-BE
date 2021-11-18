from django.urls import path, include

from . import views

urlpatterns = [
    path('list/', views.music_list, name='music_list'),
    path('get_music/', views.get_music, name='get_music'),
]
