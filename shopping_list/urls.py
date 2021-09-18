
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.shopping_lists.urls')),
    path('recipes/', include('app.recipes.urls')),
    path('ingredients/', include('app.ingredients.urls')),
    path('recipe_ingredients/', include('app.recipe_ingredients.urls')),
    path('shopping_list/', include('app.shopping_list_items.urls')),
]
