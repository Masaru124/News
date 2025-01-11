from django.urls import path
from .views import register, login_view, profile, logout_view, edit_profile, forgot_password

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),  # New URL for editing profile
    path('forgot-password/', forgot_password, name='forgot_password'),  # New URL for forgot password
    path('logout/', logout_view, name='logout'),  # Add logout URL
]
