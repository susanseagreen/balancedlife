from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView
from .forms import RecipeIngredientCreateForm
from .models import RecipeIngredient
from app.recipes.models import Recipe


class RecipeIngredientCreateView(CreateView):
    template_name = 'recipe_ingredients/recipe_ingredient_create.html'

    def get(self, request, *args, **kwargs):

        recipe_ingredients = RecipeIngredient.objects\
            .select_related('code_ingredient')\
            .filter(id=self.kwargs['fk'])\
            .order_by('code_ingredient__name')
        recipes = Recipe.objects.all().order_by('category', 'name')
        recipe = recipes.filter(id=self.kwargs['fk']).first()
        form = RecipeIngredientCreateForm()

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
            instance = form.save(commit=False)
            instance.save()

            return redirect(reverse_lazy('recipe_ingredients:create', kwargs={'fk': instance.pk}))

        return redirect(self.request.META['HTTP_REFERER'])


class RecipeIngredientModalUpdateView(UpdateView):
    template_name = 'recipe_ingredients/recipe_ingredient_update_modal.html'

    def get(self, request, *args, **kwargs):

        recipe = Recipe.objects.get(id=self.kwargs['fk'])
        form = RecipeIngredientCreateForm(instance=recipe)

        context = {
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        recipe_ingredient = RecipeIngredient.objects.get(id=self.kwargs['pk'])

        form = RecipeIngredientCreateForm(request.POST, instance=recipe_ingredient)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])
