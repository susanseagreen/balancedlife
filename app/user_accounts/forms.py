from django import forms
from app.user_accounts.models import UserAccount
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from app.user_accounts.models import UserAccount
from app.shopping_lists.models import ShoppingList


class UserAccountCreateModalForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['code_user']
        labels = {'code_user': 'Share'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        filters = kwargs.get('initial', None)
        if filters:
            filters = kwargs['initial']['filters']
            self.fields['code_user'].queryset = filters['user']
        self.helper.layout = Layout(
            Row(
                Column('code_user', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row justify-content-center'
            ),
        )


class UserAccountUpdateModalForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['code_user_account']
        labels = {
            'code_user_account': 'Group'
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
                Column('code_user_account', css_class='form-group mb-0 pb-0 col'),
                css_class='form-row'
            ),
        )