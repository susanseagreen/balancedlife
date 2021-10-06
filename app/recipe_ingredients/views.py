from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import RecipeIngredientCreateForm, RecipeIngredientUpdateForm
from .models import RecipeIngredient
from app.recipes.models import Recipe
from .lib import recipe_ingredient


class RecipeIngredientCreateView(View):
    template_name = 'recipe_ingredients/recipe_ingredient_create.html'

    def get(self, request, *args, **kwargs):
        recipe_ingredients = RecipeIngredient.objects \
            .select_related('code_ingredient') \
            .filter(code_recipe_id=self.kwargs['fk']) \
            .order_by('code_ingredient__name')
        recipes = Recipe.objects.select_related('code_category').order_by('code_category', 'name')
        recipe = recipes.filter(id=self.kwargs['fk']).first()
        form = RecipeIngredientCreateForm()

        recipe_ingredient.get_fraction(recipe_ingredients)

        context = {
            'recipe_ingredients': recipe_ingredients,
            'recipes': recipes,
            'recipe': recipe,
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = RecipeIngredientCreateForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            messages.success(self.request, f"Ingredient already exists on this Recipe")

        return redirect(reverse_lazy('recipe_ingredients:create', kwargs={'fk': self.kwargs['fk']}))


class RecipeIngredientModalUpdateView(View):
    template_name = 'recipe_ingredients/recipe_ingredient_update_modal.html'

    def get(self, request, *args, **kwargs):
        recipe_ingredient = RecipeIngredient.objects.select_related('code_ingredient').get(id=self.kwargs['pk'])
        form = RecipeIngredientUpdateForm(instance=recipe_ingredient)

        context = {
            'ingredient_name': recipe_ingredient.code_ingredient.name,
            'fk': self.kwargs['fk'],
            'pk': self.kwargs['pk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        recipe_ingredient = RecipeIngredient.objects.get(id=self.kwargs['pk'])

        form = RecipeIngredientUpdateForm(request.POST, instance=recipe_ingredient)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])
