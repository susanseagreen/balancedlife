from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import (ShoppingListMealItemForm,
                    ShoppingListMealItemSelectForm,
                    ShoppingListUpdateGetMealItemForm,
                    ShoppingListUpdatePostMealItemForm,
                    ShoppingListIngredientItemForm,
                    ShoppingListUpdateGetIngredientItemForm,
                    ShoppingListUpdatePostIngredientItemForm,
                    ShoppingListUpdateOtherItemForm,
                    ShoppingListOtherItemForm)
from .models import ShoppingListItem
from app.shopping_lists.models import ShoppingList
from app.meal_categories.models import MealCategory
from app.meal_ingredients.models import MealIngredient
from app.meals.models import Meal


class ShoppingListMealItemCreateView(View):
    template_name = 'shopping_list_items/shopping_list_item_meal_create.html'

    def get(self, request, *args, **kwargs):

        form = ShoppingListMealItemForm()

        context = {
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)


class ShoppingListMealItemSelectView(View):
    template_name = 'shopping_list_items/shopping_list_item_meal_select.html'

    def get(self, request, *args, **kwargs):

        create_form = ShoppingListMealItemForm(request.GET)

        if create_form.is_valid():

            meal_id = f"meal_id:{create_form.cleaned_data['meals'].id}"
            day_of_week = f"day_of_week:{','.join(create_form.cleaned_data['day_of_week'])}"
            meal_days = f"meal:{','.join(create_form.cleaned_data['meal'])}"
            quantity = f"quantity:{create_form.cleaned_data['quantity']}"

            meal = Meal.objects \
                .get(id=create_form.cleaned_data['meals'].id)

            meal_category_dict = {}
            meal_categories = MealCategory.objects.all()
            for category in meal_categories:
                meal_category_dict[category.id] = category.name

            if ',' in meal.meal_category:
                meal_category_list = []
                meal.meal_category = meal.meal_category.split(',')
                for meal_category in meal.meal_category:
                    meal_category_list.append(meal_category_dict[int(meal_category)])
            else:
                meal_category_list = [meal_category_dict[int(meal.meal_category)]]

            meal.meal_category = meal_category_list

            meal_ingredients = MealIngredient.objects \
                .filter(code_meal_id=int(create_form.cleaned_data['meals'].id)) \
                .values_list('id', 'code_ingredient__name')

            if meal_ingredients:

                filters = {"meal_ingredients": meal_ingredients}

                select_form = ShoppingListMealItemSelectForm(initial={'filters': filters})

                context = {
                    'fk': kwargs['fk'],
                    'meal': meal,
                    'create_data': f"{meal_id}|{day_of_week}|{meal_days}|{quantity}",
                    'select_form': select_form,
                }

                return render(request, template_name=self.template_name, context=context)

            messages.success(self.request, "There are no ingredients loaded on this meal")

        messages.success(self.request, "Something went wrong")

        return redirect(reverse_lazy('shopping_lists:update', kwargs={'pk': self.kwargs['fk']}))

    def post(self, request, *args, **kwargs):

        results = request.GET['create_data'].split('|')
        create_data = {}
        for result in results:
            label, values = result.split(':')
            if ',' in values:
                values = values.split(',')
            create_data[label] = values

        meal_ingredients = MealIngredient.objects \
            .filter(code_meal_id=create_data['meal_id']) \
            .values_list('id', 'code_ingredient__name')

        filters = {"meal_ingredients": meal_ingredients}

        select_form = ShoppingListMealItemSelectForm(request.POST, initial={'filters': filters})

        if select_form.is_valid():
            meal_servings = Meal.objects.get(id=create_data['meal_id']).servings
            quantity = int(create_data['quantity'])
            ingredients = select_form.cleaned_data['meal_ingredients']

            if not quantity:
                quantity = (len(create_data['day_of_week']) * len(create_data['meal'])) or 1
            if not create_data['day_of_week']:
                day_of_week = '0'
            else:
                day_of_week = ','.join(create_data['day_of_week'])
            if not create_data['meal']:
                meal = '0'
            else:
                meal = ','.join(create_data['meal'])
            if meal_servings:
                quantity = quantity / meal_servings

            meal_ingredients = MealIngredient.objects.filter(code_meal_id=create_data['meal_id'])
            for meal_ingredient in meal_ingredients:
                if str(meal_ingredient.id) in ingredients:
                    added = True
                else:
                    added = False
                ShoppingListItem.objects.create(
                    code_shopping_list_id=self.kwargs['fk'],
                    code_ingredient_id=meal_ingredient.code_ingredient_id,
                    code_meal_ingredient_id=meal_ingredient.id,
                    measurement_value=meal_ingredient.measurement_value,
                    measurement_type=meal_ingredient.measurement_type,
                    quantity=quantity,
                    day_of_week=day_of_week,
                    meal=meal,
                    added=added,
                )

        return redirect(reverse_lazy('shopping_lists:update', kwargs={'pk': self.kwargs['fk']}))


class ShoppingListIngredientItemCreateView(View):
    template_name = 'shopping_list_items/shopping_list_item_ingredient_create.html'

    def get(self, request, *args, **kwargs):
        form = ShoppingListIngredientItemForm()

        context = {
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ShoppingListIngredientItemForm(request.POST)

        if form.is_valid():
            day_of_week = ','.join(form.cleaned_data['day_of_week'])
            meal = ','.join(form.cleaned_data['meal'])
            quantity = form.cleaned_data['quantity']
            if not quantity:
                quantity = len(form.cleaned_data['day_of_week']) or len(form.cleaned_data['meal']) or 1
            if not day_of_week:
                day_of_week = '0'
            if not meal:
                meal = '0'
            ShoppingListItem.objects.create(
                code_shopping_list_id=self.kwargs['fk'],
                code_ingredient_id=form.cleaned_data['ingredient'].pk,
                code_meal_ingredient_id=None,
                measurement_value=form.cleaned_data['measurement_value'],
                measurement_type=form.cleaned_data['measurement_type'],
                quantity=quantity,
                day_of_week=day_of_week,
                meal=meal,
            )

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListIngredientItemUpdateView(View):
    template_name = 'shopping_list_items/shopping_list_item_ingredient_update.html'

    def get(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['pk'])
        form = ShoppingListUpdateGetIngredientItemForm(instance=shopping_list_item)

        context = {
            'pk': self.kwargs['pk'],
            'shopping_list_item': shopping_list_item,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['pk'])

        form = ShoppingListUpdatePostIngredientItemForm(request.POST, instance=shopping_list_item)

        if form.is_valid():
            day_of_week = ','.join(form.cleaned_data['day_of_week'])
            meal = ','.join(form.cleaned_data['meal'])
            quantity = form.cleaned_data['quantity']
            if not quantity:
                quantity = len(form.cleaned_data['day_of_week']) or len(form.cleaned_data['meal']) or 1
            if not day_of_week:
                day_of_week = '0'
            if not meal:
                meal = '0'
            instance = form.save(commit=False)
            instance.day_of_week = day_of_week
            instance.meal = meal
            instance.quantity = quantity
            instance.save()

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListMealItemUpdateView(View):
    template_name = 'shopping_list_items/shopping_list_item_meal_update.html'

    def get(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['fk'])
        form = ShoppingListUpdateGetMealItemForm(instance=shopping_list_item)

        context = {
            'fk': self.kwargs['fk'],
            'meal_name': shopping_list_item.code_meal_ingredient.code_meal.name,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['fk'])

        form = ShoppingListUpdatePostMealItemForm(request.POST, instance=shopping_list_item)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListOtherItemCreateView(View):
    template_name = 'shopping_list_items/shopping_list_item_other_create.html'

    def get(self, request, *args, **kwargs):
        form = ShoppingListOtherItemForm()

        context = {
            'fk': self.kwargs['fk'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ShoppingListOtherItemForm(request.POST)

        if form.is_valid():
            ShoppingListItem.objects.create(
                code_shopping_list_id=self.kwargs['fk'],
                measurement_value=form.cleaned_data['measurement_value'],
                name=form.cleaned_data['name'],
                code_ingredient_id=None,
            )

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListOtherItemUpdateView(View):
    template_name = 'shopping_list_items/shopping_list_item_other_update.html'

    def get(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['fk'])
        form = ShoppingListUpdateOtherItemForm(instance=shopping_list_item)

        context = {
            'fk': self.kwargs['fk'],
            'shopping_list_item': shopping_list_item,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        shopping_list_item = ShoppingListItem.objects.get(id=self.kwargs['fk'])

        form = ShoppingListUpdateOtherItemForm(request.POST, instance=shopping_list_item)

        if form.is_valid():
            form.save()

        return redirect(self.request.META['HTTP_REFERER'])


class ShoppingListDeleteMealView(View):
    template_name = 'shopping_list_items/shopping_list_item_meal_delete.html'

    def get(self, request, *args, **kwargs):

        shopping_list = ShoppingList.objects.get(id=self.kwargs['fk'])

        shopping_list_items = ShoppingListItem.objects \
            .select_related('code_ingredient') \
            .filter(
                code_shopping_list_id=self.kwargs['fk'],
                code_meal_ingredient__code_meal_id=self.kwargs['meal_id'],
                added=True
            ).order_by('code_ingredient__name')

        context = {
            'shopping_list': shopping_list,
            'shopping_list_items': shopping_list_items,
            'fk': self.kwargs['fk'],
            'meal_id': self.kwargs['meal_id'],
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        shopping_list_items = ShoppingListItem.objects \
            .filter(
                code_shopping_list_id=self.kwargs['fk'],
                code_meal_ingredient__code_meal_id=self.kwargs['meal_id'],
                added=True
            )

        for shopping_list_item in shopping_list_items:
            shopping_list_item.added = False
            shopping_list_item.save()

        return redirect(self.request.META['HTTP_REFERER'])
