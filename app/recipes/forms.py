from django import forms
from app.recipes.models import Recipe, RecipeIngredient
from django.forms.models import inlineformset_factory


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'


RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeCreateForm, extra=1, can_delete=False)
