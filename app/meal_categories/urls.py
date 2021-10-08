from django.urls import path
from .views import MealCategoryCreateView, MealCategoryModalUpdateView


app_name = "meal_categories"


urlpatterns = [
    path('create/', MealCategoryCreateView.as_view(), name='create'),
    path('update_modal/<pk>', MealCategoryModalUpdateView.as_view(), name='update_modal'),
]
