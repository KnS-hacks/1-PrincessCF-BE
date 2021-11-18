from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Music
from .serializers import MusicSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def music_list(request):
    if request.method == 'POST':
        music_serializer = MusicSerializer(data=request.data)
        if music_serializer.is_valid(raise_exception=True):
            music_serializer.save()
            return Response(music_serializer.data)
    else:
        musics = Music.objects.filter(is_not_played=True).order_by('id')
        music_serializer = MusicSerializer(musics, many=True)
        return Response(music_serializer.data)