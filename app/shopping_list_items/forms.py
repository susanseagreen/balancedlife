from django import forms
from common.choices import measurement_type_choices
from app.meals.models import Meal
from app.ingredients.models import Ingredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from .models import ShoppingListItem
from django_select2.forms import Select2Widget
from common.choices import days_of_week, meals as meal_choices


class ShoppingListMealItemForm(forms.Form):
    meals = forms.ModelChoiceField(queryset=Meal.objects.order_by('name'), widget=Select2Widget)
    day_of_week = forms.MultipleChoiceField(choices=days_of_week, initial='0', widget=forms.CheckboxSelectMultiple, required=False)
    meal = forms.MultipleChoiceField(choices=meal_choices, initial='0', widget=forms.CheckboxSelectMultiple, required=False)
    quantity = forms.IntegerField(initial=1, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('quantity', css_class='d-none'),
            Row(
                Column('meals', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('day_of_week', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('meal', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListIngredientItemForm(forms.Form):
    measurement_value = forms.DecimalField(label='Amount', initial=1, max_digits=5, decimal_places=2, required=False)
    measurement_type = forms.ChoiceField(label='Measurement', choices=measurement_type_choices, widget=Select2Widget, required=False)
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.order_by('name'))
    day_of_week = forms.MultipleChoiceField(choices=days_of_week, initial='0', widget=forms.CheckboxSelectMultiple, required=False)
    meal = forms.MultipleChoiceField(choices=meal_choices, initial='0', widget=forms.CheckboxSelectMultiple, required=False)
    quantity = forms.IntegerField(initial=1, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('quantity', css_class='d-none'),
            Row(
                Column('measurement_value', css_class='form-group col-4 mb-0 pb-0'),
                Column('measurement_type', css_class='form-group col-8 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ingredient', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('day_of_week', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('meal', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdateGetIngredientItemForm(forms.ModelForm):
    measurement_value = forms.DecimalField(label='Amount', max_digits=5, decimal_places=2, required=False)
    measurement_type = forms.ChoiceField(label='Measurement', choices=measurement_type_choices, widget=Select2Widget, required=False)
    ingredient = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}), required=False)
    day_of_week = forms.MultipleChoiceField(choices=days_of_week, widget=forms.CheckboxSelectMultiple, required=False)
    meal = forms.MultipleChoiceField(choices=meal_choices, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = ShoppingListItem
        fields = ['added', 'quantity', 'measurement_value', 'measurement_type', 'code_ingredient', 'day_of_week', 'meal']
        labels = {
            'added': '',
            'code_ingredient': 'Ingredient',
            'measurement_value': 'Amount',
            'measurement_type': 'Measurement',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        if ',' in self.initial['day_of_week']:
            self.initial['day_of_week'] = self.initial['day_of_week'].split(',')
        self.fields['day_of_week'].initial = [self.initial['day_of_week']]

        if ',' in self.initial['meal']:
            self.initial['meal'] = self.initial['meal'].split(',')
        self.fields['meal'].initial = [self.initial['meal']]

        self.fields['ingredient'].initial = Ingredient.objects.get(id=self.initial['code_ingredient']).name

        self.helper.layout = Layout(
            Row(
                Column('added', css_class='form-group col-1 mb-0 pb-0 fake-label'),
                Column('measurement_value', css_class='form-group col-3 mb-0 pb-0'),
                Column('measurement_type', css_class='form-group col-8 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ingredient', css_class='form-group col-sm-10 col-12 mb-0 pb-0'),
                Column('quantity', css_class='form-group col-sm-2 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('day_of_week', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('meal', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdatePostIngredientItemForm(forms.ModelForm):
    measurement_value = forms.DecimalField(label='Amount', max_digits=5, decimal_places=2, required=False)
    measurement_type = forms.ChoiceField(label='Measurement', choices=measurement_type_choices, widget=Select2Widget, required=False)
    ingredient = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}), required=False)
    day_of_week = forms.MultipleChoiceField(choices=days_of_week, widget=forms.CheckboxSelectMultiple, required=False)
    meal = forms.MultipleChoiceField(choices=meal_choices, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = ShoppingListItem
        fields = ['added', 'quantity', 'measurement_value', 'measurement_type', 'day_of_week', 'meal']
        labels = {
            'added': '',
            'code_ingredient': 'Ingredient',
            'measurement_value': 'Amount',
            'measurement_type': 'Measurement',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('added', css_class='form-group col-1 mb-0 pb-0 fake-label'),
                Column('measurement_value', css_class='form-group col-3 mb-0 pb-0'),
                Column('measurement_type', css_class='form-group col-8 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ingredient', css_class='form-group col-sm-10 col-12 mb-0 pb-0'),
                Column('quantity', css_class='form-group col-sm-2 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('day_of_week', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('meal', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdateOtherItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}), required=False)

    class Meta:
        model = ShoppingListItem
        fields = ['added', 'measurement_value', 'name']
        labels = {
            'added': '',
            'measurement_value': 'Amount',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column('added', css_class='form-group col-1 mb-0 pb-0 fake-label'),
                Column('measurement_value', css_class='form-group col-3 mb-0 pb-0'),
                Column('name', css_class='form-group col-8 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdateIngredientItemForm(forms.ModelForm):
    measurement_value = forms.DecimalField(label='Amount', initial=1, max_digits=5, decimal_places=2, required=False)
    measurement_type = forms.ChoiceField(label='Measurement', choices=measurement_type_choices, widget=Select2Widget, required=False)
    day_of_week = forms.MultipleChoiceField(choices=days_of_week, widget=forms.CheckboxSelectMultiple, required=False)
    meal = forms.MultipleChoiceField(choices=meal_choices, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = ShoppingListItem
        fields = ['added', 'quantity', 'measurement_value', 'measurement_type', 'code_ingredient', 'day_of_week', 'meal']
        labels = {
            'added': '',
            'code_ingredient': 'Ingredient',
            'measurement_value': 'Amount',
            'measurement_type': 'Measurement',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('added', css_class='form-group col-1 mb-0 pb-0 fake-label'),
                Column('measurement_value', css_class='form-group col-3 mb-0 pb-0'),
                Column('measurement_type', css_class='form-group col-8 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ingredient', css_class='form-group col-sm-10 col-12 mb-0 pb-0'),
                Column('quantity', css_class='form-group col-sm-2 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('day_of_week', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('meal', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListOtherItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['name', 'measurement_value']
        labels = {
            'measurement_value': 'Quantity',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['measurement_value'].initial = 1
        self.helper.layout = Layout(
            Row(
                Column('measurement_value', css_class='form-group col-sm-2 col-4 mb-0 pb-0'),
                Column('name', css_class='form-group col-sm-10 col-8 mb-0 pb-0'),
                css_class='form-row'
            ),
        )
