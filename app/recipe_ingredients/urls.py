from django.urls import path
from app.recipe_ingredients.views import RecipeIngredientCreateView, RecipeIngredientModalUpdateView

app_name = "recipe_ingredients"

urlpatterns = [
    path('create/<fk>', RecipeIngredientCreateView.as_view(), name='create'),
    path('update_modal/<fk>/<pk>', RecipeIngredientModalUpdateView.as_view(), name='update_modal'),
]
