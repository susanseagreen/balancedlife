from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import MealIngredientCreateForm, MealIngredientUpdateForm
from .models import MealIngredient
from app.meals.models import Meal
from .lib import meal_ingredient
from common import categories


class MealIngredientCreateView(View):
    template_name = 'meal_ingredients/meal_ingredient_create.html'

    def get(self, request, *args, **kwargs):
        meal_ingredients = MealIngredient.objects \
            .select_related('code_ingredient') \
            .filter(code_meal_id=self.kwargs['fk']) \
            .order_by('code_ingredient__name')
        meals = Meal.objects.order_by('name')

        meal = meals.filter(id=self.kwargs['fk']).first()
        if ',' in meal.meal_category:
            meal.meal_category = meal.meal_category.split(',')

        meal_category_dict = categories.build_meal_category_dict()
        meal.meal_categories = []
        for meal_category in meal.meal_category:
            meal.meal_categories.append(meal_category_dict[meal_category])

        form = MealIngredientCreateForm()

        meal_ingredient.get_fraction(meal_ingredients)

        context = {
            'meal_ingredients': meal_ingredients,
            'meals': meals,
            'meal': meal,
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = MealIngredientCreateForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            messages.success(self.request, f"Ingredient already exists on this Meal")

        return redirect(reverse_lazy('meal_ingredients:create', kwargs={'fk': self.kwargs['fk']}))


class MealIngredientModalUpdateView(View):
    template_name = 'meal_ingredients/meal_ingredient_update_modal.html'

    def get(self, request, *args, **kwargs):
        meal_ingredient = MealIngredient.objects.select_related('code_ingredient').order_by('code_ingredient__name').get(id=self.kwargs['pk'])
        form = MealIngredientUpdateForm(instance=meal_ingredient)

        context = {
            'ingredient_name': meal_ingredient.code_ingredient.name,
            'fk': self.kwargs['fk'],
            'pk': self.kwargs['pk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        meal_ingredient = MealIngredient.objects.get(id=self.kwargs['pk'])

        form = MealIngredientUpdateForm(request.POST, instance=meal_ingredient)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])