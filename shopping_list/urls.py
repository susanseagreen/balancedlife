from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('app.registration.urls')),
    path('meals/', include('app.meals.urls')),
    path('meal_categories/', include('app.meal_categories.urls')),
    path('meal_ingredients/', include('app.meal_ingredients.urls')),
    path('ingredient_categories/', include('app.ingredient_categories.urls')),
    path('ingredients/', include('app.ingredients.urls')),
    path('shopping_list/', include('app.shopping_lists.urls')),
    path('shopping_list_items/', include('app.shopping_list_items.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
