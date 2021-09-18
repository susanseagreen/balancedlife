from django.urls import path
from app.shopping_lists.views import ShoppingListCreateView, ShoppingListUpdateView


app_name = "shopping_lists"


urlpatterns = [
    path('', ShoppingListCreateView.as_view(), name='create'),
    path('update/<pk>', ShoppingListUpdateView.as_view(), name='update'),
]
