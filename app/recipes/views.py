from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView
from .forms import RecipeCreateForm, RecipeIngredientFormSet
from .models import Recipe, RecipeIngredient


class RecipeCreateView(CreateView):
    template_name = 'recipes/recipe_create.html'

    def get(self, request, *args, **kwargs):

        recipes = Recipe.objects.all().order_by('category', 'name')
        form = RecipeCreateForm()

        context = {
            'recipes': recipes,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = RecipeCreateForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return redirect(reverse_lazy('recipes:update', kwargs={'pk': instance.pk}))

        return redirect(self.request.META['HTTP_REFERER'])


class RecipeUpdateView(UpdateView):
    template_name = 'recipes/recipe_update.html'
    model = Recipe
    fields = ['id', 'name']
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)

        context['recipes'] = Recipe.objects.order_by('category', 'name')
        if self.object:
            context['recipe'] = Recipe.objects.get(id=self.object.id)

        if self.request.POST:
            context['recipe_ingredients'] = RecipeIngredientFormSet(
                self.request.POST, queryset=RecipeIngredient.objects.all(), instance=self.object)
            context['recipe_ingredients'].full_clean()
        else:
            recipe_ingredient = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.all(), instance=self.object)
            context['recipe_ingredients'] = recipe_ingredient

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['recipe_ingredients']

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return redirect(self.request.META['HTTP_REFERER'])

        else:
            messages.error(self.request, 'Something went wrong')
            return super().form_invalid(form)
