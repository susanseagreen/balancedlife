from django.urls import path
from app.shopping_list_items.views import ShoppingListRecipeItemCreateView, ShoppingListIngredientItemCreateView, ShoppingListItemModalUpdateView

app_name = "shopping_list_items"

urlpatterns = [
    path('create_recipe_modal/<fk>', ShoppingListRecipeItemCreateView.as_view(), name='create_recipe_modal'),
    path('create_ingredient_modal/<fk>', ShoppingListIngredientItemCreateView.as_view(), name='create_ingredient_modal'),
    path('update_ingredient_modal/<pk>', ShoppingListItemModalUpdateView.as_view(), name='update_ingredient_modal'),
]
