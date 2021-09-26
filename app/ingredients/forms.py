from django import forms
from app.ingredients.models import Ingredient


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