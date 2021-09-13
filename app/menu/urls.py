from django.urls import path, include
from .views import MenuView


urlpatterns = [
    path('', MenuView.as_view(), name='home'),
]
