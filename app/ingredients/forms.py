from django import forms
from app.ingredients.models import Ingredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name', 'category', 'brand']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-lg-6 col-sm-12'),
                Column('category', css_class='form-group col-lg-3 col-sm-12'),
                Column('brand', css_class='form-group col-lg-3 col-sm-12'),
                css_class='form-row'
            ),
        )
