from django.urls import path
from app.recipes.views import RecipeCreateView, RecipeUpdateView

app_name = "recipes"

urlpatterns = [
    path('create/', RecipeCreateView.as_view(), name='create'),
    path('update/<pk>', RecipeUpdateView.as_view(), name='update'),
]
