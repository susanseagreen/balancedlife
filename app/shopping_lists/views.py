from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShoppingListCreateForm, ShoppingListUpdateDatesForm, ShoppingListUpdateNoDatesForm
from .models import ShoppingList
from .lib import shopping_list_items, user_accounts
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.user_accounts.models import UserAccount


class ShoppingListCreateView(View):
    template_name = 'shopping_lists/shopping_list_create.html'

    def get(self, request, *args, **kwargs):

        user_accounts_list = user_accounts.get_user_accounts(self)
        user_account_ids, user_account_choices = user_accounts.build_lookup_dict(self, user_accounts_list)
        user_account_tuple = user_accounts.build_user_account_tuple(user_account_choices)

        filters = {
            'user_account_tuple': user_account_tuple,
        }

        form = ShoppingListCreateForm(initial={'filters': filters})

        context = {
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ShoppingListCreateForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.date_from:
                instance.date_to = instance.date_from + timedelta(days=6)
            instance.save()

            return redirect(reverse_lazy('shopping_lists:update', kwargs={'pk': instance.pk}))

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListUpdateView(View):
    template_name = 'shopping_lists/shopping_list_update.html'

    def get(self, request, *args, **kwargs):

        meal_list = []
        ingredient_list = {}
        meals_search = self.request.GET.get('meals_search') or ''

        shopping_list_items.build_shopping_list(self, ingredient_list)

        user_accounts_list = user_accounts.get_user_accounts(self)
        user_account_ids, user_account_choices = user_accounts.build_lookup_dict(self, user_accounts_list)
        user_account_tuple = user_accounts.build_user_account_tuple(user_account_choices)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        filters = {
            'user_account_tuple': user_account_tuple,
            'user_account_id': shopping_list.code_user_account_id,
        }

        for key, meal in ingredient_list.items():
            for meal_added in meal['added']:
                meal_names = meal_added['code_meal_ingredient__code_meal__name']
                if meal_names and meal_names not in meal_list:
                    if meals_search.lower() in meal_names.lower():
                        meal_list.append(meal_names)

        if shopping_list.date_from:
            form = ShoppingListUpdateDatesForm(initial={'filters': filters}, instance=shopping_list)
        else:
            form = ShoppingListUpdateNoDatesForm(initial={'filters': filters}, instance=shopping_list)

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

        return redirect(self.request.META['HTTP_REFERER'])


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


class UserAccountShoppingListModalCreateView(View):
    template_name = 'shopping_list/user_account_create_modal.html'

    def get(self, request, *args, **kwargs):

        form = UserAccountCreateModalForm()

        user_accounts = UserAccount.objects.all()

        context = {
            'pk': kwargs['shopping_list_id'],
            'user_accounts': user_accounts,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = UserAccountCreateModalForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.code_shopping_list_id = kwargs['shopping_list_id']
            instance.save()

        return redirect(self.request.META['HTTP_REFERER'])


class UserAccountShoppingListModalUpdateView(View):
    template_name = 'shopping_list/user_account_update_modal.html'

    def get(self, request, *args, **kwargs):

        user_accounts = UserAccount.objects.select_related('code_user_account').filter(id=kwargs['pk'])

        context = {
            'shopping_list_id': kwargs['shopping_list_id'],
            'user_accounts': user_accounts,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        user_accounts = UserAccount.objects.filter(code_shopping_list_id=kwargs['shopping_list_id'])
        for user_account in user_accounts:
            if str(user_account.id) in self.request.POST:
                user_account.is_active = True
            else:
                user_account.is_active = False
            user_account.save()

        return redirect(self.request.META['HTTP_REFERER'])
