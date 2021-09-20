from django.urls import path, include
from .views import register, user_activate, resend_activation_email, superuser_activate


urlpatterns = [
    path('register/', register, name='register'),
    path('user_activate/<user_id>/<user_code>', user_activate, name='user_activate'),
    path('superuser_activate/<user_id>/<user_code>', superuser_activate, name='superuser_activate'),
    path('resend_activation_email', resend_activation_email, name='resend_activation_email'),
]
