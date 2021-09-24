from django import forms
from app.ingredients.models import Ingredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }


class IngredientModalForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }