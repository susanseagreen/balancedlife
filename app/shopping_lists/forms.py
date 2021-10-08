from django import forms
from app.shopping_lists.models import ShoppingList
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class ShoppingListCreateForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['name', 'date_from']

        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].initial = "Shopping List"
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-sm col-12 mb-0 pb-0'),
                Column('date_from', css_class='form-group col-sm-5 col-md-4 col-12 mb-0 pb-0'),
                Submit('submit', 'Create', css_class='form-group btn btn-dark inline-btn fake-label col-sm-2 mw-65 col-12'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdateForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['name', 'date_from', 'date_to']
        labels = {'name': ''}

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row justify-content-center'
            ),
            Row(
                Column('date_from', css_class='form-group col-sm col-12 mb-0 pb-0'),
                Column('date_to', css_class='form-group col-sm-5 col-md-4 col-12 mb-0 pb-0'),
                Submit('submit', 'Update', css_class='form-group btn btn-dark inline-btn fake-label col-sm-2 mw-65 col-12'),
                css_class='form-row justify-content-center'
            ),
        )
