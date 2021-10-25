from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShoppingListCreateForm, ShoppingListUpdateDatesForm, ShoppingListUpdateNoDatesForm
from .models import ShoppingList
from app.shopping_list_items.models import ShoppingListItem
from app.common import shopping_list_items
from datetime import timedelta


class ShoppingListCreateView(View):
    template_name = 'shopping_lists/shopping_list_create.html'

    def get(self, request, *args, **kwargs):

        form = ShoppingListCreateForm()

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

        meal_list = {}
        ingredient_list = {}
        meals_search = self.request.GET.get('meals_search') or ''

        shopping_list_items.build_shopping_list(self, ingredient_list)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        for key, meal in ingredient_list.items():
            for meal_added in meal['added']:
                meal_id = meal_added['code_meal_ingredient__code_meal_id']
                meal_name = meal_added['code_meal_ingredient__code_meal__name']
                if meal_name and meal_name not in meal_list:
                    if meals_search.lower() in meal_name.lower():
                        meal_list[meal_id] = meal_name

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


class ShoppingListUpdateModalView(View):
    template_name = 'shopping_lists/shopping_list_update_modal.html'

    def get(self, request, *args, **kwargs):

        ingredient_list = {}

        shopping_list_items.build_shopping_list(self, ingredient_list)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        if shopping_list.date_from:
            form = ShoppingListUpdateDatesForm(instance=shopping_list)
        else:
            form = ShoppingListUpdateNoDatesForm(instance=shopping_list)

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list': shopping_list,
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
        ingredient_summary = shopping_list_items.build_summary(self, ingredient_list)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list': shopping_list,
            'ingredient_summary': ingredient_summary,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        shopping_list.is_active = False
        shopping_list.save()

        return redirect(reverse_lazy('home'))


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


class ShoppingListDeleteView(View):
    template_name = 'shopping_lists/shopping_list_delete.html'

    def get(self, request, *args, **kwargs):

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list': shopping_list,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        ShoppingListItem.objects.filter(code_shopping_list_id=self.kwargs['pk']).delete()
        ShoppingList.objects.filter(id=self.kwargs['pk']).delete()
        messages.success(self.request, "Shopping List deleted")

        return redirect(self.request.META['HTTP_REFERER'])
