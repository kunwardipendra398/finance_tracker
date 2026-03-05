from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language

# Language switch URL
urlpatterns = [
    path('set_language/', set_language, name='set_language'),
]

# Main URLs (with language prefix like /en/)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),      # Tracker app
    path('users/', include('users.urls')),  # Users app
   path('accounts/', include('django.contrib.auth.urls')),
)

# Media files (only in DEBUG mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)