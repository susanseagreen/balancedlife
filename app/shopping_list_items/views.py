from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import (ShoppingListMealItemForm,
                    ShoppingListIngredientItemForm,
                    ShoppingListUpdateGetIngredientItemForm,
                    ShoppingListUpdatePostIngredientItemForm,
                    ShoppingListUpdateOtherItemForm,
                    ShoppingListOtherItemForm)
from .models import ShoppingListItem
from app.meal_ingredients.models import MealIngredient
from app.meals.models import Meal


class ShoppingListMealItemCreateView(View):
    template_name = 'shopping_list_items/shopping_list_item_meal_create.html'

    def get(self, request, *args, **kwargs):

        form = ShoppingListMealItemForm()

        context = {
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = ShoppingListMealItemForm(request.POST)
        meal_servings = Meal.objects.get(id=kwargs['fk']).servings

        if form.is_valid():
            day_of_week = ','.join(form.cleaned_data['day_of_week'])
            meal = ','.join(form.cleaned_data['meal'])
            quantity = form.cleaned_data['quantity']
            if not quantity:
                quantity = len(form.cleaned_data['day_of_week']) or len(form.cleaned_data['meal']) or 1
            if not day_of_week:
                day_of_week = '0'
            if not meal:
                meal = '0'
            if meal_servings:
                quantity = meal_servings / quantity

            meal_ingredients = MealIngredient.objects.filter(code_meal_id=kwargs['fk'])
            for meal_ingredient in meal_ingredients:
                if meal_ingredient.code_ingredient.name.lower() != 'water':
                    ShoppingListItem.objects.create(
                        code_shopping_list_id=self.kwargs['fk'],
                        code_ingredient_id=meal_ingredient.code_ingredient_id,
                        code_meal_ingredient_id=meal_ingredient.id,
                        measurement_value=meal_ingredient.measurement_value,
                        measurement_type=meal_ingredient.measurement_type,
                        quantity=quantity,
                        day_of_week=day_of_week,
                        meal=meal,
                    )
                else:
                    message = "Water wasn't added to shopping list"
                    messages.success(self.request, message)

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListIngredientItemCreateView(View):
    template_name = 'shopping_list_items/shopping_list_item_ingredient_create.html'

    def get(self, request, *args, **kwargs):
        form = ShoppingListIngredientItemForm()

        context = {
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ShoppingListIngredientItemForm(request.POST)

        if form.is_valid():
            day_of_week = ','.join(form.cleaned_data['day_of_week'])
            meal = ','.join(form.cleaned_data['meal'])
            quantity = form.cleaned_data['quantity']
            if not quantity:
                quantity = len(form.cleaned_data['day_of_week']) or len(form.cleaned_data['meal']) or 1
            if not day_of_week:
                day_of_week = '0'
            if not meal:
                meal = '0'
            ShoppingListItem.objects.create(
                code_shopping_list_id=self.kwargs['fk'],
                code_ingredient_id=form.cleaned_data['ingredient'].pk,
                code_meal_ingredient_id=None,
                measurement_value=form.cleaned_data['measurement_value'],
                measurement_type=form.cleaned_data['measurement_type'],
                quantity=quantity,
                day_of_week=day_of_week,
                meal=meal,
            )

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListIngredientItemUpdateView(View):
    template_name = 'shopping_list_items/shopping_list_item_ingredient_update.html'

    def get(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['pk'])
        form = ShoppingListUpdateGetIngredientItemForm(instance=shopping_list_item)

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list_item': shopping_list_item,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['pk'])

        form = ShoppingListUpdatePostIngredientItemForm(request.POST, instance=shopping_list_item)

        if form.is_valid():
            day_of_week = ','.join(form.cleaned_data['day_of_week'])
            meal = ','.join(form.cleaned_data['meal'])
            quantity = form.cleaned_data['quantity']
            if not quantity:
                quantity = len(form.cleaned_data['day_of_week']) or len(form.cleaned_data['meal']) or 1
            if not day_of_week:
                day_of_week = '0'
            if not meal:
                meal = '0'
            instance = form.save(commit=False)
            instance.day_of_week = day_of_week
            instance.meal = meal
            instance.quantity = quantity
            instance.save()

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListOtherItemCreateView(View):
    template_name = 'shopping_list_items/shopping_list_item_other_create.html'

    def get(self, request, *args, **kwargs):
        form = ShoppingListOtherItemForm()

        context = {
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ShoppingListOtherItemForm(request.POST)

        if form.is_valid():
            ShoppingListItem.objects.create(
                code_shopping_list_id=self.kwargs['fk'],
                measurement_value=form.cleaned_data['measurement_value'],
                name=form.cleaned_data['name'],
                code_ingredient_id=None,
            )

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListOtherItemUpdateView(View):
    template_name = 'shopping_list_items/shopping_list_item_other_update.html'

    def get(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['pk'])
        form = ShoppingListUpdateOtherItemForm(instance=shopping_list_item)

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list_item': shopping_list_item,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['pk'])

        form = ShoppingListUpdateOtherItemForm(request.POST, instance=shopping_list_item)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])
