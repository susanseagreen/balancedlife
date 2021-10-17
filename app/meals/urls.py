from django.urls import path
from app.meals.views import MealCreateView, MealUpdateView, MealListView

app_name = "meals"

urlpatterns = [
    path('list/', MealListView.as_view(), name='list'),
    path('create/', MealCreateView.as_view(), name='create'),
    path('update/<pk>', MealUpdateView.as_view(), name='update'),
]
