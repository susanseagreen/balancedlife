
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('app.registration.urls')),
    path('', include('app.shopping_lists.urls')),
    path('meals/', include('app.meals.urls')),
    path('meal_categories/', include('app.meal_categories.urls')),
    path('meal_ingredients/', include('app.meal_ingredients.urls')),
    path('ingredient_categories/', include('app.ingredient_categories.urls')),
    path('ingredients/', include('app.ingredients.urls')),
    path('shopping_list/', include('app.shopping_list_items.urls')),
]
