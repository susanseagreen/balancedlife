from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import MealCategoryCreateModalForm, MealCategoryUpdateModalForm
from .models import MealCategory
from app.meals.models import Meal


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
            instance = form.save(commit=False)
            instance.code_user_account_id = self.request.user.code_user_account_name.id
            instance.save()

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

        if self.request.user.code_user_account_name.id == meal_category.code_user_account_id:

            form = MealCategoryUpdateModalForm(request.POST, instance=meal_category)

            if form.is_valid():
                form.save()

        else:
            messages.success(self.request, "Only the user that created this can edit it")

        return redirect(self.request.META['HTTP_REFERER'])
