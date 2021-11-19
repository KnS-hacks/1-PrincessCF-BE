from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse

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


@api_view(['POST'])
def get_music(request):
    if request.mehod == 'POST':
        if request.POST['who'] != None and request.POST['who'] == 'ningpop':
            musics = Music.objects.filter(is_not_played=True).order_by('id')

            if len(musics) == 0:  # 신청곡이 없을 때
                return HttpResponse("", content_type="application/text")

            music = musics[0]
            msg = f"{music.artist} {music.title}"
            music.is_not_played = False
            music.save()
            return HttpResponse(msg, content_type="application/text")
        return HttpResponse(status=404)
    else:
        return HttpResponse(status=400)