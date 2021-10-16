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
                Column('name', css_class='form-group col-7 mb-0 pb-0'),
                Column('date_from', css_class='form-group col-sm-5 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdateDatesForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['is_active', 'name', 'date_from', 'date_to']
        labels = {
            'is_active': '',
            'name': '',
        }

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
                Column('is_active', css_class='form-group mr-2 mb-0 pb-0 fake-label'),
                Column('name', css_class='form-group mb-0 pb-0 fake-label col'),
                css_class='form-row mb-0'
            ),
            Row(
                Column('date_from', css_class='form-group col-sm-6 col-12 mb-0 pb-0'),
                Column('date_to', css_class='form-group col-sm-6 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdateNoDatesForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['is_active', 'name', 'date_from']
        labels = {
            'is_active': '',
            'name': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
            'date_from': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('is_active', css_class='form-group mr-2 mb-0 pb-0 fake-label'),
                Column('name', css_class='form-group mb-0 pb-0 fake-label col'),
                Column('date_from', css_class='form-group col-sm-5 col-12 mb-0 pb-0 toggle_dates'),
                HTML('<a class="cursor-pointer button_toggle_dates btn btn-dark text-light mw-45 fake-label mr-1" title="Date">+</a>'),
                css_class='form-row'
            ),
        )
