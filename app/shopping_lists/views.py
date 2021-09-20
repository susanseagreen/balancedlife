from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShoppingListCreateForm, ShoppingListUpdateForm
from .models import ShoppingList
from .lib import shopping_list_items


class ShoppingListCreateView(View):
    template_name = 'shopping_lists/shopping_list_create.html'

    def get(self, request, *args, **kwargs):
        shopping_lists = ShoppingList.objects.order_by('name')
        form = ShoppingListCreateForm()

        context = {
            'shopping_lists': shopping_lists,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ShoppingListCreateForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return redirect(reverse_lazy('shopping_lists:update', kwargs={'pk': instance.pk}))

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListUpdateView(View):
    template_name = 'shopping_lists/shopping_list_update.html'

    def get(self, request, *args, **kwargs):

        ingredient_list = {}

        shopping_list_items.build_shopping_list(self, ingredient_list)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        form = ShoppingListUpdateForm(instance=shopping_list)

        context = {
            'pk': self.kwargs['pk'],
            'ingredient_list': ingredient_list,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        shopping_list = ShoppingList.objects.get(id=self.kwargs['pk'])

        form = ShoppingListUpdateForm(request.POST, instance=shopping_list)

        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('shopping_lists:create', kwargs={'fk': self.kwargs['pk']}))
