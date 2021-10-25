from django.urls import path
from app.shopping_lists.views import \
    ShoppingListCreateView, ShoppingListUpdateView, ShoppingListUpdateModalView, \
    ShoppingListView, ShoppingListFoodDiaryView, ShoppingListDeleteView

app_name = "shopping_lists"

urlpatterns = [

    path('create', ShoppingListCreateView.as_view(), name='create'),
    path('update/<pk>', ShoppingListUpdateView.as_view(), name='update'),
    path('update_modal/<pk>', ShoppingListUpdateModalView.as_view(), name='update_modal'),
    path('list/<pk>', ShoppingListView.as_view(), name='list'),
    path('food_diary/<pk>', ShoppingListFoodDiaryView.as_view(), name='food_diary'),
    path('delete/<pk>', ShoppingListDeleteView.as_view(), name='delete'),
]
