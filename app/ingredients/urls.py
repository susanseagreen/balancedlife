from django.urls import path
from app.ingredients.views import IngredientCreateView, IngredientUpdateView, IngredientModalCreateView, IngredientModalUpdateView


app_name = "ingredients"


urlpatterns = [
    path('create/', IngredientCreateView.as_view(), name='create'),
    path('update/<pk>', IngredientUpdateView.as_view(), name='update'),
    path('create_modal/', IngredientModalCreateView.as_view(), name='create_modal'),
    path('update_modal/<pk>', IngredientModalUpdateView.as_view(), name='update_modal'),
]
