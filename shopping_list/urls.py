
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('app.registration.urls')),
    path('', include('app.shopping_lists.urls')),
    path('recipes/', include('app.recipes.urls')),
    path('recipe_categories/', include('app.recipe_categories.urls')),
    path('recipe_ingredients/', include('app.recipe_ingredients.urls')),
    path('ingredient_categories/', include('app.ingredient_categories.urls')),
    path('ingredients/', include('app.ingredients.urls')),
    path('shopping_list/', include('app.shopping_list_items.urls')),
]
