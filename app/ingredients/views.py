from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import IngredientForm, IngredientModalForm
from .models import Ingredient
from app.meals.models import Meal
from app.ingredient_categories.models import IngredientCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class IngredientCreateView(View):
    template_name = 'ingredients/ingredient_create.html'

    def get(self, request, *args, **kwargs):

        ingredients_search = self.request.GET.get('ingredients_search') or ''

        ingredients = Ingredient.objects \
            .select_related('code_category') \
            .filter(
                Q(name__icontains=ingredients_search) |
                Q(code_category__name__icontains=ingredients_search)
            ) \
            .order_by('code_category__name', 'name')

        form = IngredientForm()

        paginator = Paginator(ingredients, 50)
        page_num = request.GET.get('page', 1)

        try:
            ingredients = paginator.get_page(page_num)
        except PageNotAnInteger:
            ingredients = paginator.get_page(1)
        except EmptyPage:
            ingredients = paginator.get_page(paginator.num_pages)

        context = {
            'ingredients_search': ingredients_search,
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

        ingredient = Ingredient.objects.get(id=kwargs['pk'])

        form = IngredientForm(instance=ingredient)

        context = {
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

        # return redirect(self.request.META['HTTP_REFERER'])
        return redirect(reverse_lazy('ingredients:create'))
