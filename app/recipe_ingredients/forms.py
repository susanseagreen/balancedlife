from django import forms
from app.recipe_ingredients.models import RecipeIngredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from django_select2.forms import Select2Widget
from app.ingredients.models import Ingredient


class RecipeIngredientCreateForm(forms.ModelForm):

    code_ingredient = forms.ModelChoiceField(
        label='Ingredient', queryset=Ingredient.objects.order_by('name'), widget=Select2Widget)

    class Meta:
        model = RecipeIngredient
        fields = ['code_recipe', 'added', 'measurement_value', 'measurement_type', 'code_ingredient', 'description']
        labels = {
            'added': '',
            'description': 'Preparation',
            'measurement_value': 'Amount',
            'measurement_type': '',
        }
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Chopped / Diced / Sliced / Cooked / Raw'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                HTML('<input type="hidden" name="code_recipe" id="id_code_recipe" value="{{ fk }}">'),
                Column('added', css_class='form-group col-sm-1 col-1 fake-label mb-0'),
                Column('measurement_value', css_class='form-group col-4 mb-0'),
                Column('measurement_type', css_class='form-group col-7 fake-label mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('code_ingredient', css_class='form-group col-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-12 mb-0'),
                css_class='form-row'
            ),
        )


class RecipeIngredientUpdateForm(forms.ModelForm):

    class Meta:
        model = RecipeIngredient
        fields = ['added', 'measurement_value', 'measurement_type']
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
                Column('added', css_class='form-group col-sm-1 col-1 fake-label'),
                Column('measurement_value', css_class='form-group col-sm-2 col-3'),
                Column('measurement_type', css_class='form-group col-sm-3 col-8'),
                HTML('<div class="col form-group col-sm-6 col-12">'),
                HTML('<div id="div_id_ingredient_name" class="form-group">'),
                HTML('<label for="id_ingredient_name">Ingredient</label><div class="">'),
                HTML('<input type="text" value="{{ ingredient_name }}" readonly="" class="form-control">'),
                HTML('</div></div></div>'),
                css_class='form-row'
            ),
        )
