from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import IngredientForm, IngredientModalForm
from .models import Ingredient
from app.recipes.models import Recipe


class IngredientCreateView(View):
    template_name = 'ingredients/ingredient_create.html'

    def get(self, request, *args, **kwargs):

        recipes = Recipe.objects.select_related('code_category').order_by('code_category__name', 'name')
        ingredients = Ingredient.objects.all().order_by('name')

        form = IngredientForm()

        context = {
            'recipes': recipes,
            'ingredients': ingredients,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = IngredientForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            messages.success(self.request, "The ingredient already exists")

        return redirect(reverse_lazy('ingredients:create'))


class IngredientUpdateView(View):
    template_name = 'ingredients/ingredient_update.html'

    def get(self, request, *args, **kwargs):

        recipes = Recipe.objects.select_related('code_category').order_by('code_category__name', 'name')
        ingredient = Ingredient.objects.get(id=kwargs['pk'])

        form = IngredientForm(instance=ingredient)

        context = {
            'recipes': recipes,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        ingredient = Ingredient.objects.get(id=kwargs['pk'])

        form = IngredientForm(request.POST, instance=ingredient)

        if form.is_valid():
            form.save()
        else:
            messages.success(self.request, "The ingredient already exists")

        return redirect(reverse_lazy('ingredients:create'))


class IngredientModalCreateView(View):
    template_name = 'ingredients/ingredient_create_modal.html'

    def get(self, request, *args, **kwargs):

        form = IngredientModalForm()

        context = {
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = IngredientModalForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])


class IngredientModalUpdateView(View):
    template_name = 'ingredients/ingredient_update_modal.html'

    def get(self, request, *args, **kwargs):

        ingredient = Ingredient.objects.get(id=kwargs['pk'])

        form = IngredientModalForm(instance=ingredient)

        context = {
            'pk': kwargs['pk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        ingredient = Ingredient.objects.get(id=kwargs['pk'])

        form = IngredientModalForm(request.POST, instance=ingredient)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])
