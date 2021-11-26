from django import forms
from app.ingredient_categories.models import IngredientCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class IngredientCategoryCreateModalForm(forms.ModelForm):

    class Meta:
        model = IngredientCategory
        fields = ['name', 'order']
        labels = {'name': '', 'order': ''}

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('order', css_class='form-group mw-70 mb-0 pb-0'),
                Column('name', css_class='form-group col-sm-8 col-lg-4 col-10 mb-0 pb-0'),
                Submit('submit', 'Create', css_class='form-group btn btn-dark inline-btn col-sm-2 col-lg-1 col-12'),
                css_class='form-row justify-content-center'
            ),
        )


class IngredientCategoryUpdateModalForm(forms.ModelForm):

    class Meta:
        model = IngredientCategory
        fields = ['name', 'order']
        labels = {'name': '', 'order': ''}

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('order', css_class='form-group mw-70 mb-0 pb-0'),
                Column('name', css_class='form-group col mb-0 pb-0'),
                css_class='form-row justify-content-center'
            ),
        )
