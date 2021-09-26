from django.urls import path
from app.shopping_lists.views import ShoppingListCreateView, ShoppingListUpdateView, ShoppingListView


app_name = "shopping_lists"


urlpatterns = [
    path('', ShoppingListCreateView.as_view(), name='create'),
    path('shopping_list/update/<pk>', ShoppingListUpdateView.as_view(), name='update'),
    path('shopping_list/<pk>', ShoppingListView.as_view(), name='list'),
]
