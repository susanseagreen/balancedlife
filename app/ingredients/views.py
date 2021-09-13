from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import IngredientCreateForm
from .models import Ingredient


class IngredientCreateView(View):
    template_name = 'ingredients/ingredient_create.html'

    def get(self, request, *args, **kwargs):

        ingredients = Ingredient.objects.all().order_by('name')

        form = IngredientCreateForm()

        context = {
            'ingredients': ingredients,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = IngredientCreateForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('ingredients:create'))


class IngredientUpdateView(View):
    template_name = 'ingredients/ingredient_update.html'

    def get(self, request, *args, **kwargs):

        ingredient = Ingredient.objects.get(id=kwargs['pk'])

        form = IngredientCreateForm(instance=ingredient)

        context = {
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = IngredientCreateForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('ingredients:create'))
