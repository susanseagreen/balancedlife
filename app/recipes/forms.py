from django import forms
from app.recipes.models import Recipe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'steps': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'image': 'Image URL'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('image', css_class='form-group col-12 mb-0 pb-0'),
                Column('name', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('servings', css_class='form-group col-sm-3 col-12 mb-0 pb-0'),
                Column('pax_serving', css_class='form-group col-sm-3 col-12 mb-0 pb-0'),
                Column('code_category', css_class='form-group col-sm-6 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-12 mb-0 pb-0'),
                Column('steps', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )
