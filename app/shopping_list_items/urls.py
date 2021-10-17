from django.urls import path
from app.shopping_list_items.views import (ShoppingListMealItemCreateView,
                                           ShoppingListMealItemSelectView,
                                           ShoppingListIngredientItemCreateView,
                                           ShoppingListIngredientItemUpdateView,
                                           ShoppingListOtherItemCreateView,
                                           ShoppingListOtherItemUpdateView)

app_name = "shopping_list_items"

urlpatterns = [
    path('create_meal_modal/<fk>', ShoppingListMealItemCreateView.as_view(), name='create_meal_modal'),
    path('select_meal_modal/<fk>', ShoppingListMealItemSelectView.as_view(), name='select_meal_modal'),

    path('create_ingredient_modal/<fk>', ShoppingListIngredientItemCreateView.as_view(),
         name='create_ingredient_modal'),
    path('update_ingredient_modal/<pk>', ShoppingListIngredientItemUpdateView.as_view(),
         name='update_ingredient_modal'),

    path('create_item_modal/<fk>', ShoppingListOtherItemCreateView.as_view(), name='create_item_modal'),
    path('update_item_modal/<fk>', ShoppingListOtherItemUpdateView.as_view(), name='update_item_modal'),
]
