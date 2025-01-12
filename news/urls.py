from django.contrib import admin
from django.urls import path, include
from newsletter.views import welcome

urlpatterns = [
    path('', include('newsletter.urls')), 
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include user-related URLs
]
