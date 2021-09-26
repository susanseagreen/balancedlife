from django import forms
from common.choices import measurement_type_choices
from app.recipes.models import Recipe
from app.ingredients.models import Ingredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from .models import ShoppingListItem
from django_select2.forms import Select2Widget
from common.choices import days_of_week, meals


class ShoppingListRecipeItemForm(forms.Form):

    recipe = forms.ModelChoiceField(queryset=Recipe.objects.order_by('name'), widget=Select2Widget)
    day_of_week = forms.MultipleChoiceField(choices=days_of_week, widget=forms.CheckboxSelectMultiple, required=False)
    meal = forms.MultipleChoiceField(choices=meals, widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('recipe', css_class='form-group col-12 mb-0 pb-0'),
                Column('day_of_week', css_class='form-group col-12 mb-0 pb-0'),
                Column('meal', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListIngredientItemForm(forms.Form):

    measurement_value = forms.DecimalField(label='Amount', max_digits=5, decimal_places=2, required=False)
    measurement_type = forms.ChoiceField(label='Measurement', choices=measurement_type_choices, required=False)
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.order_by('name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('measurement_value', css_class='form-group col-4 mb-0 pb-0'),
                Column('measurement_type', css_class='form-group col-8 mb-0 pb-0'),
                Column('ingredient', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdateItemForm(forms.ModelForm):

    # measurement_value = forms.DecimalField(label='Amount', max_digits=5, decimal_places=2, required=False)
    # measurement_type = forms.ChoiceField(label='Measurement', choices=measurement_type_choices, required=False)

    class Meta:
        model = ShoppingListItem
        fields = ['added', 'measurement_value', 'measurement_type']
        labels = {
            'added': '',
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
        )
