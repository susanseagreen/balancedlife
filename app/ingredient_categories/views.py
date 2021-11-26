from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import IngredientCategoryCreateModalForm, IngredientCategoryUpdateModalForm
from .models import IngredientCategory
from app.meals.models import Meal


class IngredientCategoryCreateView(View):
    template_name = 'ingredient_categories/ingredient_category_create.html'

    def get(self, request, *args, **kwargs):

        form = IngredientCategoryCreateModalForm()

        ingredient_categories = IngredientCategory.objects.order_by('name')

        context = {
            'ingredient_categories': ingredient_categories,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = IngredientCategoryCreateModalForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])


class IngredientCategoryModalUpdateView(View):
    template_name = 'ingredient_categories/ingredient_category_update_modal.html'

    def get(self, request, *args, **kwargs):

        ingredient_category = IngredientCategory.objects.get(id=kwargs['pk'])

        form = IngredientCategoryUpdateModalForm(instance=ingredient_category)

        context = {
            'pk': kwargs['pk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        ingredient_category = IngredientCategory.objects.get(id=kwargs['pk'])

        form = IngredientCategoryUpdateModalForm(request.POST, instance=ingredient_category)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])
