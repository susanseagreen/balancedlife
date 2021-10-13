from django.urls import path
from app.shopping_lists.views import ShoppingListCreateView, ShoppingListUpdateView, ShoppingListView, ShoppingListFoodDiaryView

app_name = "shopping_lists"

urlpatterns = [

    path('create', ShoppingListCreateView.as_view(), name='create'),
    path('update/<pk>', ShoppingListUpdateView.as_view(), name='update'),
    path('list/<pk>', ShoppingListView.as_view(), name='list'),
    path('food_diary/<pk>', ShoppingListFoodDiaryView.as_view(), name='food_diary'),
]
