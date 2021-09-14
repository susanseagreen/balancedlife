from django import forms
from app.ingredients.models import Ingredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name', 'food_group', 'brand']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
            'food_group': forms.TextInput(attrs={'list': 'datalist'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-lg-6 col-sm-12'),
                Column('food_group', css_class='form-group col-lg-3 col-sm-12'),
                HTML('<datalist id="datalist">'),
                HTML('<option value="Vegetable">'),
                HTML('<option value="Meat">'),
                HTML('<option value="Diary">'),
                HTML('</datalist>'),
                Column('brand', css_class='form-group col-lg-3 col-sm-12'),
                css_class='form-row'
            ),
        )


class IngredientModalForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name', 'food_group', 'brand']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
            'food_group': forms.TextInput(attrs={'list': 'datalist'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-12'),
                Column('food_group', css_class='form-group col-12'),
                HTML('<datalist id="datalist">'),
                HTML('<option value="Diary">'),
                HTML('<option value="Fruit">'),
                HTML('<option value="Grain">'),
                HTML('<option value="Other">'),
                HTML('<option value="Protein">'),
                HTML('<option value="Veg">'),
                HTML('</datalist>'),
                Column('brand', css_class='form-group col-12'),
                css_class='form-row'
            ),
        )
