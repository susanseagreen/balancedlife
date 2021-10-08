from django.urls import path
from app.meals.views import MealCreateView, MealUpdateView

app_name = "meals"

urlpatterns = [
    path('create/', MealCreateView.as_view(), name='create'),
    path('update/<pk>', MealUpdateView.as_view(), name='update'),
]
