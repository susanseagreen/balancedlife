from django import forms
from app.shared_accounts.models import SharedAccount
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from app.shared_accounts.models import SharedAccount


class SharedAccountCreateModalForm(forms.ModelForm):
    class Meta:
        model = SharedAccount
        fields = ['code_user']
        labels = {'code_user': 'Add user'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        exclude_users = SharedAccount.objects.filter(
            code_shopping_list_id=self.instance.code_shopping_list_id).values_list('code_user_id', flat=True)
        self.fields['code_user'].queryset = self.fields['code_user'].queryset.exclude(id__in=exclude_users)
        self.helper.layout = Layout(
            Row(
                Column('code_user', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row justify-content-center'
            ),
        )
