from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import RecipeForm
from .models import Recipe


class RecipeCreateView(View):
    template_name = 'recipes/recipe_create.html'

    def get(self, request, *args, **kwargs):

        recipes = Recipe.objects.select_related('code_category').order_by('name')
        form = RecipeForm()

        context = {
            'recipes': recipes,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = RecipeForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return redirect(reverse_lazy('recipe_ingredients:create', kwargs={'fk': instance.pk}))

        return redirect(self.request.META['HTTP_REFERER'])


class RecipeUpdateView(View):
    template_name = 'recipes/recipe_update.html'

    def get(self, request, *args, **kwargs):

        recipes = Recipe.objects.select_related('code_category').order_by('name')
        recipe = Recipe.objects.get(id=self.kwargs['pk'])
        form = RecipeForm(instance=recipe)

        context = {
            'recipes': recipes,
            'recipe': recipe,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        recipe = Recipe.objects.get(id=self.kwargs['pk'])

        form = RecipeForm(request.POST, instance=recipe)

        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('recipe_ingredients:create', kwargs={'fk': self.kwargs['pk']}))
