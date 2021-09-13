from django import forms
from app.ingredients.models import Ingredient


class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'
