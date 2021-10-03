from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import RecipeCategoryCreateModalForm, RecipeCategoryUpdateModalForm
from .models import RecipeCategory
from app.recipes.models import Recipe


class RecipeCategoryCreateView(View):
    template_name = 'recipe_categories/recipe_category_create.html'

    def get(self, request, *args, **kwargs):

        form = RecipeCategoryCreateModalForm()

        recipe_categories = RecipeCategory.objects.order_by('name')

        context = {
            'recipe_categories': recipe_categories,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = RecipeCategoryCreateModalForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])


class RecipeCategoryModalUpdateView(View):
    template_name = 'recipe_categories/recipe_category_update_modal.html'

    def get(self, request, *args, **kwargs):

        recipe_category = RecipeCategory.objects.get(id=kwargs['pk'])

        form = RecipeCategoryUpdateModalForm(instance=recipe_category)

        context = {
            'pk': kwargs['pk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        recipe_category = RecipeCategory.objects.get(id=kwargs['pk'])

        form = RecipeCategoryUpdateModalForm(request.POST, instance=recipe_category)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])
