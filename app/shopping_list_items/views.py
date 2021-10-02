from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShoppingListRecipeItemForm, ShoppingListIngredientItemForm, ShoppingListUpdateItemForm
from .models import ShoppingListItem
from app.recipe_ingredients.models import RecipeIngredient


class ShoppingListRecipeItemCreateView(View):
    template_name = 'shopping_list_items/shopping_list_item_recipe_create.html'

    def get(self, request, *args, **kwargs):

        form = ShoppingListRecipeItemForm()

        context = {
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = ShoppingListRecipeItemForm(request.POST)

        if form.is_valid():
            recipe = form.cleaned_data['recipe']
            day_of_week = ','.join(form.cleaned_data['day_of_week'])
            meal = ','.join(form.cleaned_data['meal'])
            recipe_ingredients = RecipeIngredient.objects.filter(code_recipe_id=recipe.pk)
            for recipe_ingredient in recipe_ingredients:
                if recipe_ingredient.code_ingredient.name.lower() != 'water':
                    ShoppingListItem.objects.create(
                        code_shopping_list_id=self.kwargs['fk'],
                        code_ingredient_id=recipe_ingredient.code_ingredient_id,
                        code_recipe_ingredient_id=recipe_ingredient.id,
                        measurement_value=recipe_ingredient.measurement_value,
                        measurement_type=recipe_ingredient.measurement_type,
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
        day_of_week = str(','.join(form.cleaned_data['day_of_week']))
        meal = str(','.join(form.cleaned_data['meal']))

        if form.is_valid():
            ShoppingListItem.objects.create(
                code_shopping_list_id=self.kwargs['fk'],
                code_ingredient_id=form.cleaned_data['ingredient'].pk,
                code_recipe_ingredient_id=None,
                measurement_value=form.cleaned_data['measurement_value'],
                measurement_type=form.cleaned_data['measurement_type'],
                day_of_week=day_of_week,
                meal=meal,
            )

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListItemModalUpdateView(View):
    template_name = 'shopping_list_items/shopping_list_item_update.html'

    def get(self, request, *args, **kwargs):

        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['pk'])
        form = ShoppingListUpdateItemForm(instance=shopping_list_item)

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list_item': shopping_list_item,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['pk'])

        form = ShoppingListUpdateItemForm(request.POST, instance=shopping_list_item)
        day_of_week = str(','.join(form.cleaned_data['day_of_week']))
        meal = str(','.join(form.cleaned_data['meal']))

        if form.is_valid():
            instance = form.save(commit=False)
            instance.day_of_week = day_of_week
            instance.meal = meal
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])
