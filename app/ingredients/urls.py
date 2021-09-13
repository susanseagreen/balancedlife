from django.urls import path
from app.ingredients.views import IngredientCreateView, IngredientUpdateView


app_name = "ingredients"


urlpatterns = [
    path('create/', IngredientCreateView.as_view(), name='create'),
    path('update/<pk>', IngredientUpdateView.as_view(), name='update'),
]
