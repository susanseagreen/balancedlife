from django import forms
from app.shopping_lists.models import ShoppingList
from app.user_accounts.models import UserAccount
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class ShoppingListCreateForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['name', 'date_from', 'code_user_account']

        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'code_user_account': 'Group'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].initial = "Shopping List"
        filters = kwargs.get('initial', None)
        if filters:
            filters = kwargs['initial']['filters']
            self.fields['code_user_account'].choices = tuple(filters['user_account_tuple'])
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-7 mb-0 pb-0'),
                Column('date_from', css_class='form-group col-sm-5 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('code_user_account', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class ShoppingListUpdateDatesForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['is_active', 'name', 'date_from', 'date_to', 'code_user_account']
        labels = {
            'is_active': '',
            'name': '',
            'code_user_account': 'Group'
        }

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        filters = kwargs.get('initial', None)
        if filters:
            filters = kwargs['initial']['filters']
            self.fields['code_user_account'].choices = tuple(filters['user_account_tuple'])
            self.fields['code_user_account'].initial = filters['user_account_id']
        self.helper.layout = Layout(
            Row(
                Column('is_active', css_class='form-group mr-2 mb-0 pb-0 fake-label'),
                Column('name', css_class='form-group mb-0 pb-0 fake-label col'),
                css_class='form-row mb-0'
            ),
            Row(
                Column('code_user_account', css_class='form-group mb-0 pb-0 col-12'),
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
        fields = ['is_active', 'name', 'date_from', 'code_user_account']
        labels = {
            'is_active': '',
            'name': '',
            'code_user_account': 'Group'
        }

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
            'date_from': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        filters = kwargs.get('initial', None)
        if filters:
            filters = kwargs['initial']['filters']
            self.fields['code_user_account'].choices = tuple(filters['user_account_tuple'])
            self.fields['code_user_account'].initial = filters['user_account_id']
        self.helper.layout = Layout(
            Row(
                Column('is_active', css_class='form-group mr-2 mb-0 pb-0 fake-label'),
                Column('name', css_class='form-group mb-0 pb-0 fake-label col'),
                Column('date_from', css_class='form-group col-sm-5 col-12 mb-0 pb-0 toggle_dates'),
                HTML('<a class="cursor-pointer button_toggle_dates btn btn-dark text-light mw-45 fake-label mr-1" title="Date">+</a>'),
                css_class='form-row'
            ),
            Row(
                Column('code_user_account', css_class='form-group mb-0 pb-0 col'),
                css_class='form-row'
            ),
        )


class UserAccountShoppingListCreateModalForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['code_user']
        labels = {'code_user': 'Share'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        exclude_users = UserAccount.objects.filter(
            code_shopping_list_id=self.instance.code_shopping_list_id).values_list('code_user_id', flat=True)
        self.fields['code_user'].queryset = self.fields['code_user'].queryset.exclude(id__in=exclude_users)
        self.helper.layout = Layout(
            Row(
                Column('code_user', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row justify-content-center'
            ),
        )
