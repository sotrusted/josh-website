from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from core.utils import extract_youtube_id


class Page(models.Model):
    """Editable flat page: bio, services, lessons, sheet-music, orchestra."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text='URL key, e.g. "bio" → /bio/')
    content = HTMLField()
    hero_image = models.ImageField(upload_to='pages/', blank=True, null=True)
    hero_image_caption = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=True)
    nav_order = models.PositiveSmallIntegerField(default=10, help_text='Lower = earlier in nav')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nav_order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})


class Video(models.Model):
    """YouTube embed for the Video page."""

    title = models.CharField(max_length=200)
    youtube_url = models.CharField(
        max_length=200,
        default='',
        help_text='Paste the full YouTube URL, e.g. https://www.youtube.com/watch?v=…',
    )
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    @property
    def video_id(self):
        return extract_youtube_id(self.youtube_url)

    @property
    def embed_url(self):
        vid = self.video_id
        return f'https://www.youtube.com/embed/{vid}' if vid else ''


class BandcampEmbed(models.Model):
    """
    A featured media item on the Listen page / homepage.
    Use embed_code for Bandcamp iframes OR youtube_url for YouTube — not both.
    """

    title = models.CharField(max_length=200)
    embed_code = models.TextField(
        blank=True,
        help_text='Bandcamp: paste the full &lt;iframe&gt; embed code from Share/Embed',
    )
    youtube_url = models.CharField(
        max_length=200,
        blank=True,
        help_text='YouTube: paste the full video URL — leave blank if using Bandcamp embed code',
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    @property
    def youtube_embed_url(self):
        vid = extract_youtube_id(self.youtube_url)
        return f'https://www.youtube.com/embed/{vid}' if vid else ''
