from django.shortcuts import render
from blog.models import Post
from pages.models import BandcampEmbed


def home(request):
    recent_posts = Post.objects.filter(is_published=True).order_by('-published_at')[:3]
    embeds = BandcampEmbed.objects.filter(is_active=True)
    return render(request, 'home.html', {
        'recent_posts': recent_posts,
        'embeds': embeds,
    })
