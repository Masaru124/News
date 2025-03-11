from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from newsletter.views import welcome

urlpatterns = [
    path('', include('newsletter.urls')), 
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include user-related URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
