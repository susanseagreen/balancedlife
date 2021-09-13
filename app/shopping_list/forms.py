from django import forms
from app.shopping_list.models import ShoppingList


class ShoppingListCreateForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = '__all__'
