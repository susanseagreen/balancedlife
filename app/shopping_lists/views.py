from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShoppingListCreateForm, ShoppingListUpdateDatesForm, ShoppingListUpdateNoDatesForm
from .models import ShoppingList
from app.meals.models import Meal
from .lib import shopping_list_items
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.shared_accounts.models import SharedAccount


class ShoppingListCreateView(View):
    template_name = 'shopping_lists/shopping_list_create.html'

    def get(self, request, *args, **kwargs):

        meals_search = self.request.GET.get('meals_search') or ''
        meals = Meal.objects.filter(name__icontains=meals_search).order_by('name')

        # shared_accounts = SharedAccount.objects.filter(code_user_id=self.request.user.id, is_active=True)
        shared_accounts = SharedAccount.objects.filter(is_active=True)

        shared_accounts_list = {}
        for shared_account in shared_accounts:
            shopping_list_id = shared_account.code_shopping_list_id
            if shopping_list_id not in shared_accounts_list:
                shared_accounts_list[shopping_list_id] = []
            shared_accounts_list[shopping_list_id].append(shared_account.code_user.username)

        shopping_lists = ShoppingList.objects.filter(id__in=shared_accounts).order_by('name', 'is_active')

        for shopping_list in shopping_lists:
            shopping_list.shared_account_names = shared_accounts_list[shopping_list.id]

        form = ShoppingListCreateForm()

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
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ShoppingListCreateForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.date_from:
                instance.code_user_id = self.request.user.id
                instance.date_to = instance.date_from + timedelta(days=6)
            instance.save()

            shared_account = SharedAccount()
            shared_account.code_user_id = self.request.user.id
            shared_account.code_shopping_lists_id = instance.id
            shared_account.save()

            return redirect(reverse_lazy('shopping_lists:update', kwargs={'pk': instance.pk}))

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListUpdateView(View):
    template_name = 'shopping_lists/shopping_list_update.html'

    def get(self, request, *args, **kwargs):

        meal_list = []
        ingredient_list = {}
        meals_search = self.request.GET.get('meals_search') or ''

        shopping_list_items.build_shopping_list(self, ingredient_list)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        for key, meal in ingredient_list.items():
            for meal_added in meal['added']:
                meal_names = meal_added['code_meal_ingredient__code_meal__name']
                if meal_names and meal_names not in meal_list:
                    if meals_search.lower() in meal_names.lower():
                        meal_list.append(meal_names)

        if shopping_list.date_from:
            form = ShoppingListUpdateDatesForm(instance=shopping_list)
        else:
            form = ShoppingListUpdateNoDatesForm(instance=shopping_list)

        context = {
            'pk': self.kwargs['pk'],
            'meals_search': meals_search,
            'shopping_list': shopping_list,
            'meal_list': meal_list,
            'ingredient_list': ingredient_list,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        if shopping_list.date_from:
            form = ShoppingListUpdateDatesForm(request.POST, instance=shopping_list)
        else:
            form = ShoppingListUpdateNoDatesForm(request.POST, instance=shopping_list)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.date_from:
                instance.date_to = instance.date_from + timedelta(days=6)
            else:
                instance.date_to = None
            instance.save()

        return redirect(reverse_lazy('shopping_lists:update', kwargs={'pk': self.kwargs['pk']}))


class ShoppingListView(View):
    template_name = 'shopping_lists/shopping_list.html'

    def get(self, request, *args, **kwargs):
        ingredient_list = {}

        shopping_list_items.build_shopping_list(self, ingredient_list)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list': shopping_list,
            'ingredient_list': ingredient_list,
        }

        return render(request, template_name=self.template_name, context=context)


class ShoppingListFoodDiaryView(View):
    template_name = 'shopping_lists/shopping_list_food_diary.html'

    def get(self, request, *args, **kwargs):
        food_diary = {}

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        shopping_list_items.build_diary(food_diary)
        shopping_list_items.build_food_diary(self, food_diary)

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list': shopping_list,
            'food_diary': food_diary,
        }

        return render(request, template_name=self.template_name, context=context)
