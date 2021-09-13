from django.urls import path
from app.shopping_list.views import ShoppingListListView, ShoppingListCreateView, ShoppingListUpdateView


app_name = "shopping_lists"


urlpatterns = [
    path('list/', ShoppingListListView.as_view(), name='list'),
    path('create/', ShoppingListCreateView.as_view(), name='create'),
    path('update/<pk>', ShoppingListUpdateView.as_view(), name='update'),
]
