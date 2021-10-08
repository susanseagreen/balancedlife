from django import forms
from app.meal_categories.models import MealCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class MealCategoryCreateModalForm(forms.ModelForm):

    class Meta:
        model = MealCategory
        fields = ['name']
        labels = {'name': ''}

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-sm-10 col-lg-6 col-12 mb-0 pb-0'),
                Submit('submit', 'Create', css_class='form-group btn btn-dark inline-btn col-sm-2 col-lg-1 col-12'),
                css_class='form-row justify-content-center'
            ),
        )


class MealCategoryUpdateModalForm(forms.ModelForm):

    class Meta:
        model = MealCategory
        fields = ['name']
        labels = {'name': ''}

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row justify-content-center'
            ),
        )
