from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import MealCreateForm, MealUpateForm
from .models import Meal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class MealCreateView(View):
    template_name = 'meals/meal_create.html'

    def get(self, request, *args, **kwargs):

        meals_search = self.request.GET.get('meals_search') or ''
        meals = Meal.objects.filter(name__icontains=meals_search).order_by('name')

        form = MealCreateForm()

        paginator = Paginator(meals, 100)
        page_num = request.GET.get('page', 1)

        try:
            meals = paginator.get_page(page_num)
        except PageNotAnInteger:
            meals = paginator.get_page(1)
        except EmptyPage:
            meals = paginator.get_page(paginator.num_pages)

        context = {
            'meals_search': meals_search,
            'meals': meals,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        if request.FILES:
            form = MealCreateForm(request.POST, request.FILES)
        else:
            form = MealCreateForm(request.POST)

        if form.is_valid():
            meal_categories = ','.join(form.cleaned_data['meal_categories'])
            instance = form.save(commit=False)
            instance.meal_category = meal_categories
            instance.save()

            return redirect(reverse_lazy('meal_ingredients:create', kwargs={'fk': instance.pk}))

        return redirect(self.request.META['HTTP_REFERER'])


class MealUpdateView(View):
    template_name = 'meals/meal_update.html'

    def get(self, request, *args, **kwargs):

        meals_search = self.request.GET.get('meals_search') or ''
        meals = Meal.objects.filter(name__icontains=meals_search).order_by('name')

        meal = Meal.objects.get(id=self.kwargs['pk'])
        form = MealUpateForm(instance=meal)

        paginator = Paginator(meals, 100)
        page_num = request.GET.get('page', 1)

        try:
            meals = paginator.get_page(page_num)
        except PageNotAnInteger:
            meals = paginator.get_page(1)
        except EmptyPage:
            meals = paginator.get_page(paginator.num_pages)

        context = {
            'meals_search': meals_search,
            'meals': meals,
            'meal': meal,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        meal = Meal.objects.get(id=self.kwargs['pk'])

        if request.FILES:
            form = MealUpateForm(request.POST, request.FILES, instance=meal)
        else:
            form = MealUpateForm(request.POST, instance=meal)

        if form.is_valid():
            meal_categories = ','.join(form.cleaned_data['meal_categories'])
            instance = form.save(commit=True)
            instance.meal_category = meal_categories
            instance.save()

        return redirect(reverse_lazy('meal_ingredients:create', kwargs={'fk': self.kwargs['pk']}))
