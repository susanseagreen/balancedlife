from django import forms
from app.meal_ingredients.models import MealIngredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from django_select2.forms import Select2Widget
from app.ingredients.models import Ingredient


class MealIngredientCreateForm(forms.ModelForm):

    code_ingredient = forms.ModelChoiceField(
        label='Ingredient', queryset=Ingredient.objects.order_by('name'), widget=Select2Widget)

    class Meta:
        model = MealIngredient
        fields = ['code_meal', 'measurement_value', 'measurement_type', 'code_ingredient', 'preparation']
        labels = {
            'measurement_value': 'Amount',
            'measurement_type': '',
        }
        widgets = {
            'preparation': forms.TextInput(attrs={'placeholder': 'Chopped / Diced / Sliced / Cooked / Raw'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                HTML('<input type="hidden" name="code_meal" id="id_code_meal" value="{{ fk }}">'),
                Column('measurement_value', css_class='form-group col-4 mb-0'),
                Column('measurement_type', css_class='form-group col-8 fake-label mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('code_ingredient', css_class='form-group col-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('preparation', css_class='form-group col-12 mb-0'),
                css_class='form-row'
            ),
        )


class MealIngredientUpdateForm(forms.ModelForm):

    class Meta:
        model = MealIngredient
        fields = ['added', 'measurement_value', 'measurement_type', 'preparation', 'code_ingredient']
        labels = {
            'added': '',
            'measurement_value': 'Amount',
            'measurement_type': 'Measurement',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('added', css_class='form-group col-1 fake-label'),
                Column('measurement_value', css_class='form-group col-sm-2 col-4'),
                Column('measurement_type', css_class='form-group col-sm-4 col-7'),
                Column('preparation', css_class='form-group col-sm-5 col-12'),
                Column('code_ingredient', css_class='form-group col-12'),
                # HTML('<div class="col form-group col-12">'),
                # HTML('<div id="div_id_ingredient_name" class="form-group">'),
                # HTML('<label for="id_ingredient_name">Ingredient</label><div class="">'),
                # HTML('<input type="text" value="{{ ingredient_name }}" readonly="" class="form-control">'),
                # HTML('</div></div></div>'),
                css_class='form-row'
            ),
        )
