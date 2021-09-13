from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView
from .forms import RecipeIngredientFormSet
from .models import Recipe, RecipeIngredient


class RecipeCreateView(CreateView):
    template_name = 'recipes/recipe_create.html'
    model = Recipe
    fields = ['id', 'name', 'category']
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(RecipeCreateView, self).get_context_data(**kwargs)

        context['recipes'] = Recipe.objects.all().order_by('name')

        if self.request.POST:
            context['recipe_ingredient'] = RecipeIngredientFormSet(
                self.request.POST, queryset=RecipeIngredient.objects.all(), instance=self.object)
            context['recipe_ingredient'].full_clean()
        else:
            recipe_ingredient = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.all(), instance=self.object)
            context['recipe_ingredient'] = recipe_ingredient

        return context


class RecipeUpdateView(View):
    template_name = 'recipes/recipe_update.html'
    model = Recipe
    fields = ['id', 'name', 'category']

    def get(self, request, *args, **kwargs):

        recipes = Recipe.objects.get(id=kwargs['pk'])

        form = RecipeIngredientFormSet(instance=recipes)

        context = {
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = RecipeIngredientFormSet(request.POST)

        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('recipes:list'))
