from django import forms
from app.ingredients.models import Ingredient
from app.ingredient_categories.models import IngredientCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from django_select2.forms import Select2Widget


class IngredientForm(forms.ModelForm):
    code_category = forms.ModelChoiceField(label='Category', queryset=IngredientCategory.objects.order_by('name'),
                                           widget=Select2Widget)

    class Meta:
        model = Ingredient
        fields = ['name', 'code_category']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-sm-6 col-lg-8 col-12 mb-0 pb-0'),
                Column('code_category', css_class='form-group col-sm-6 col-lg-4 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class IngredientModalForm(forms.ModelForm):
    code_category = forms.ModelChoiceField(label='Category', queryset=IngredientCategory.objects.order_by('name'), widget=Select2Widget)

    class Meta:
        model = Ingredient
        fields = ['name', 'code_category']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-sm-6 col-lg-8 col-12 mb-0 pb-0'),
                Column('code_category', css_class='form-group col-sm-6 col-lg-4 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )
