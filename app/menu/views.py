from django.shortcuts import render
from django.views.generic import View
from app.recipes.models import Recipe


class MenuView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):

        recipes = Recipe.objects.all().order_by('category', 'name')

        context = {
            'recipes': recipes
        }

        return render(request, template_name=self.template_name, context=context)
