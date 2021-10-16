from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import MealCategoryCreateModalForm, MealCategoryUpdateModalForm
from .models import MealCategory


class MealCategoryCreateView(View):
    template_name = 'meal_categories/meal_category_create.html'

    def get(self, request, *args, **kwargs):

        form = MealCategoryCreateModalForm()

        meal_categories = MealCategory.objects.order_by('name')

        context = {
            'meal_categories': meal_categories,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = MealCategoryCreateModalForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])


class MealCategoryModalUpdateView(View):
    template_name = 'meal_categories/meal_category_update_modal.html'

    def get(self, request, *args, **kwargs):

        meal_category = MealCategory.objects.get(id=kwargs['pk'])

        form = MealCategoryUpdateModalForm(instance=meal_category)

        context = {
            'pk': kwargs['pk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        meal_category = MealCategory.objects.get(id=kwargs['pk'])

        form = MealCategoryUpdateModalForm(request.POST, instance=meal_category)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])
