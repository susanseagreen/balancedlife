from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from app.meals.models import Meal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .lib import shopping_list, user_accounts


class HomeView(View):
    template_name = 'shopping_list_home.html'

    def get(self, request, *args, **kwargs):

        context = {}

        if self.request.user.id:

            meals_search = self.request.GET.get('meals_search') or ''
            meals = Meal.objects.filter(name__icontains=meals_search).order_by('name')

            user_accounts_list = user_accounts.get_user_accounts(self)
            user_account_ids, user_account_choices = user_accounts.build_lookup_dict(self, user_accounts_list)
            shopping_lists = shopping_list.build_shopping_lists(user_account_ids, user_account_choices)

            paginator = Paginator(meals, 100)
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
