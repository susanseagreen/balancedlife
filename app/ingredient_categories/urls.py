from django.urls import path
from .views import IngredientCategoryCreateView, IngredientCategoryModalUpdateView


app_name = "ingredient_categories"


urlpatterns = [
    path('create/', IngredientCategoryCreateView.as_view(), name='create'),
    path('update_modal/<pk>', IngredientCategoryModalUpdateView.as_view(), name='update_modal'),
]
