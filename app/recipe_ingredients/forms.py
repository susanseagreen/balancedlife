from django import forms
from app.recipe_ingredients.models import RecipeIngredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class RecipeIngredientCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'

        labels = {
            'measurement_value': '',
            'measurement_type': '',
        }
        widgets = {
            'measurement_type': forms.TextInput(attrs={'list': 'datalist'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('measurement_value', css_class='form-group col-sm-2 col-4 fake-label'),
                Column('measurement_type', css_class='form-group col-sm-2 col-8 fake-label'),
                HTML('<datalist id="datalist">'),
                HTML('<option value="gram">'),
                HTML('<option value="kilogram">'),
                HTML('<option value="teaspoon">'),
                HTML('<option value="tablespoon">'),
                HTML('<option value="tablespoons">'),
                HTML('<option value="cup">'),
                HTML('<option value="cups">'),
                HTML('<option value="litre">'),
                HTML('<option value="litres">'),
                HTML('<option value="grams">'),
                HTML('<option value="kilograms">'),
                HTML('<option value="teaspoons">'),
                HTML('</datalist>'),
                Column('code_ingredient', css_class='form-group col-sm-8 col-12'),
                css_class='form-row'
            ),
        )
