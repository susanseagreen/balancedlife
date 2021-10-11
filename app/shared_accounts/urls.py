from django.urls import path
from .views import SharedAccountModalCreateView, SharedAccountModalUpdateView


app_name = "shared_accounts"


urlpatterns = [
    path('create_modal/<shopping_list_id>', SharedAccountModalCreateView.as_view(), name='create_modal'),
    path('update_modal/<pk>', SharedAccountModalUpdateView.as_view(), name='update_modal'),
]
