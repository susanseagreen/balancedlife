from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Row, Column


class UserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Reconfirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username',          css_class='form-group col-12 mb-0 flex-wrap'),
                Column('email',             css_class='form-group col-12 mb-0 flex-wrap'),
                Column('password1',         css_class='form-group col-12 mb-0 flex-wrap'),
                Column('password2',         css_class='form-group col-12 mb-0 flex-wrap'),
                css_class='form-row'
            ),
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=False):
        user = super(UserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
