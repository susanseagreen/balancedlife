from django.urls import path
from .views import UserAccountModalCreateView, UserAccountModalUpdateView


app_name = "user_accounts"


urlpatterns = [
    path('create_modal/<shopping_list_id>', UserAccountModalCreateView.as_view(), name='create_modal'),
    path('update_modal/<shopping_list_id>', UserAccountModalUpdateView.as_view(), name='update_modal'),
]
