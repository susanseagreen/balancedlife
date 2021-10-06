from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShoppingListCreateForm, ShoppingListUpdateForm
from .models import ShoppingList
from app.recipes.models import Recipe
from .lib import shopping_list_items
from datetime import timedelta


class ShoppingListCreateView(View):
    template_name = 'shopping_lists/shopping_list_create.html'

    def get(self, request, *args, **kwargs):
        shopping_lists = ShoppingList.objects.filter(user_id=self.request.user.id).order_by('name')
        recipes = Recipe.objects.select_related('code_category').order_by('code_category', 'name')
        form = ShoppingListCreateForm()

        context = {
            'shopping_lists': shopping_lists,
            'recipes': recipes,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ShoppingListCreateForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.date_from:
                instance.user = self.request.user.id
                instance.date_to = instance.date_from + timedelta(days=6)
            instance.save()

            return redirect(reverse_lazy('shopping_lists:update', kwargs={'pk': instance.pk}))

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListUpdateView(View):
    template_name = 'shopping_lists/shopping_list_update.html'

    def get(self, request, *args, **kwargs):

        ingredient_list = {}

        shopping_list_items.build_shopping_list(self, ingredient_list)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        form = ShoppingListUpdateForm(instance=shopping_list)

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list': shopping_list,
            'ingredient_list': ingredient_list,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        form = ShoppingListUpdateForm(request.POST, instance=shopping_list)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.date_from:
                instance.date_to = instance.date_from + timedelta(days=6)
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
