from django import forms
from common.choices import measurement_type_choices
from app.recipes.models import Recipe
from app.ingredients.models import Ingredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from .models import ShoppingListItem


class ShoppingListRecipeItemForm(forms.Form):

    recipes = forms.ModelChoiceField(queryset=Recipe.objects.order_by('name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('recipes', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListIngredientItemForm(forms.Form):

    measurement_value = forms.DecimalField(label='Amount', max_digits=5, decimal_places=2, required=False)
    measurement_type = forms.ChoiceField(label='Measurement', choices=measurement_type_choices, required=False)
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.order_by('food_group', 'name'))

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

    measurement_value = forms.DecimalField(label='Amount', max_digits=5, decimal_places=2, required=False)
    measurement_type = forms.ChoiceField(label='Measurement', choices=measurement_type_choices, required=False)

    class Meta:
        model = ShoppingListItem
        fields = ['added', 'measurement_value', 'measurement_type']
        labels = {
            'added': '',
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
