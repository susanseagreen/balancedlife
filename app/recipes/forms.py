from django import forms
from app.recipes.models import Recipe, RecipeIngredient
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeIngredientCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'

        labels = {
            'measurement_value': '',
            'measurement_type': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('code_ingredient', css_class='form-group col-9'),
                Column('measurement_value', css_class='form-group col-1 fake-label'),
                Column('measurement_type', css_class='form-group col-2 fake-label'),
                css_class='form-row'
            ),
        )


RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient, form=RecipeIngredientCreateForm, extra=1, can_delete=True)
