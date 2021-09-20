from django import forms
from app.recipe_ingredients.models import RecipeIngredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class RecipeIngredientCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['added', 'measurement_value', 'measurement_type', 'code_ingredient']
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
                Column('added', css_class='form-group col-sm-1 col-1 fake-label'),
                Column('measurement_value', css_class='form-group col-sm-2 col-3'),
                Column('measurement_type', css_class='form-group col-sm-3 col-8'),
                Column('code_ingredient', css_class='form-group col-sm-6 col-12'),
                css_class='form-row'
            ),
        )


class RecipeIngredientUpdateForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
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
                Column('added', css_class='form-group col-sm-1 col-1 fake-label'),
                Column('measurement_value', css_class='form-group col-sm-2 col-3'),
                Column('measurement_type', css_class='form-group col-sm-3 col-8'),
                HTML('<div class="col form-group col-sm-6 col-12">'),
                HTML('<div id="div_id_ingredient_name" class="form-group">'),
                HTML('<label for="id_ingredient_name">Ingredient</label><div class="">'),
                HTML('<input type="text" value="{{ ingredient_name }}" readonly="" class="form-control">'),
                HTML('</div></div></div>'),
                css_class='form-row'
            ),
        )
