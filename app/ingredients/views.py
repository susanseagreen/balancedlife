from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import IngredientForm, IngredientModalForm
from .models import Ingredient
from app.recipes.models import Recipe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IngredientCreateView(View):
    template_name = 'ingredients/ingredient_create.html'

    def get(self, request, *args, **kwargs):

        recipes = Recipe.objects.select_related('code_category').order_by('name')
        ingredients = Ingredient.objects.all().order_by('name')

        form = IngredientForm()

        paginator = Paginator(ingredients, 10)
        page_num = request.GET.get('page', 1)

        try:
            ingredients = paginator.get_page(page_num)
        except PageNotAnInteger:
            ingredients = paginator.get_page(1)
        except EmptyPage:
            ingredients = paginator.get_page(paginator.num_pages)

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

        recipes = Recipe.objects.select_related('code_category').order_by('name')
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
