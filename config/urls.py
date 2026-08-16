from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    # Specific routes first — blog and contact before the pages catch-all
    path('', include('core.urls')),
    path('', include('blog.urls')),       # news/, events/, press/, posts/<slug>/
    path('contact/', include('contact.urls')),  # contact/...
    path('', include('pages.urls')),      # video/, listen/, <slug:slug>/ — catch-all LAST
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
