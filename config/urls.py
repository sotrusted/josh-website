from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    # Serve media files in all environments (nginx handles this in real prod)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # Specific routes first — blog and contact before the pages catch-all
    path('', include('core.urls')),
    path('', include('blog.urls')),       # news/, events/, press/, posts/<slug>/
    path('contact/', include('contact.urls')),  # contact/...
    path('', include('pages.urls')),      # video/, listen/, <slug:slug>/ — catch-all LAST
]
