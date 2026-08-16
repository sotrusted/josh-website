from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request, category=None):
    posts = Post.objects.filter(is_published=True)
    if category:
        posts = posts.filter(category=category)
    label = {
        'news': 'News',
        'events': 'Events',
        'press': 'Press',
    }.get(category, 'All Posts')
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'category': category,
        'label': label,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'blog/post_detail.html', {'post': post})
