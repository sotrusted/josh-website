from django.shortcuts import render, get_object_or_404
from .models import Page, Video, BandcampEmbed


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'pages/page_detail.html', {'page': page})


def video_list(request):
    videos = Video.objects.filter(is_published=True)
    return render(request, 'pages/video_list.html', {'videos': videos})


def listen(request):
    embeds = BandcampEmbed.objects.filter(is_active=True)
    return render(request, 'pages/listen.html', {'embeds': embeds})
