
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.menu.urls')),
    path('ingredients/', include('app.ingredients.urls')),
    path('recipes/', include('app.recipes.urls')),
    path('shopping_list/', include('app.shopping_list.urls')),
]
