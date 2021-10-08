from django.urls import path
from app.meal_ingredients.views import MealIngredientCreateView, MealIngredientModalUpdateView

app_name = "meal_ingredients"

urlpatterns = [
    path('create/<fk>', MealIngredientCreateView.as_view(), name='create'),
    path('update_modal/<fk>/<pk>', MealIngredientModalUpdateView.as_view(), name='update_modal'),
]
