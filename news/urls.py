from django.contrib import admin
from django.urls import path, include
from newsletter.views import welcome

urlpatterns = [
    path('', welcome, name='welcome'),  # Welcome page
    path('index/', include('newsletter.urls')),  # Include index and other newsletter URLs
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include user-related URLs
]
