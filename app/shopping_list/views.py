from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShoppingListCreateForm
from .models import ShoppingList


class ShoppingListListView(View):
    template_name = 'shopping_lists/shopping_list_list.html'

    def get(self, request, *args, **kwargs):

        shopping_lists = ShoppingList.objects.select_related('code_recipe')\
            .values(
            'pk', 'name', 'code_recipe__name'
        )



        context = {
            'shopping_lists': shopping_lists
        }

        return render(request, template_name=self.template_name, context=context)


class ShoppingListCreateView(View):
    template_name = 'shopping_lists/shopping_list_form.html'

    def get(self, request, *args, **kwargs):

        form = ShoppingListCreateForm()

        context = {
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = ShoppingListCreateForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('shopping_lists:list'))


class ShoppingListUpdateView(View):
    template_name = 'shopping_lists/shopping_list_form.html'

    def get(self, request, *args, **kwargs):

        shopping_lists = ShoppingList.objects.get(id=kwargs['pk'])

        form = ShoppingListCreateForm(instance=shopping_lists)

        context = {
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = ShoppingListCreateForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('shopping_lists:list'))
