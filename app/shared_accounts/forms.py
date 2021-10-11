from django import forms
from app.shared_accounts.models import SharedAccount
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from app.registration.models import User
from django_select2.forms import Select2Widget


class SharedAccountCreateModalForm(forms.ModelForm):

    user = forms.ChoiceField(widget=Select2Widget(attrs={'autofocus': True}))

    class Meta:
        model = SharedAccount
        fields = ['code_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        users = User.objects.exclude(id=self.fields['code_user'].initial).order_by('username').values_list('id', 'username')
        self.fields['user'].choices = list(users)
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row justify-content-center'
            ),
        )


class SharedAccountUpdateModalForm(forms.ModelForm):

    class Meta:
        model = SharedAccount
        fields = ['code_user']
        labels = {'code_user': 'User'}

        widgets = {
            'code_user': forms.TextInput(attrs={'autofocus': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('code_user', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row justify-content-center'
            ),
        )
