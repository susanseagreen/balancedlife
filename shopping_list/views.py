from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from app.meals.models import Meal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.shopping_lists.models import ShoppingList


class HomeView(View):
    template_name = 'shopping_list_home.html'

    def get(self, request, *args, **kwargs):

        context = {}

        if self.request.user.id:

            meals_search = self.request.GET.get('meals_search') or ''
            meals = Meal.objects.filter(name__icontains=meals_search).order_by('name')
            shopping_lists = ShoppingList.objects.order_by('-is_active', 'date_from', 'name')

            paginator = Paginator(meals, 15)
            page_num = request.GET.get('page', 1)

            try:
                meals = paginator.get_page(page_num)
            except PageNotAnInteger:
                meals = paginator.get_page(1)
            except EmptyPage:
                meals = paginator.get_page(paginator.num_pages)

            context = {
                'meals_search': meals_search,
                'shopping_lists': shopping_lists,
                'meals': meals,
            }

        return render(request, template_name=self.template_name, context=context)
