from django.urls import path
from .views import RecipeCategoryCreateView, RecipeCategoryModalUpdateView


app_name = "recipe_categories"


urlpatterns = [
    path('create/', RecipeCategoryCreateView.as_view(), name='create'),
    path('update_modal/<pk>', RecipeCategoryModalUpdateView.as_view(), name='update_modal'),
]
