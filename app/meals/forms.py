from django import forms
from app.meals.models import Meal
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from app.meal_categories.models import MealCategory


class MealCreateForm(forms.ModelForm):

    categories = MealCategory.objects.order_by('name').values_list('id', 'name')

    # meal_categories = forms.MultipleChoiceField(choices=list(categories), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Meal
        fields = ['image', 'name', 'servings', 'pax_serving', 'description', 'steps']

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
                css_class='form-row'
            ),
            Row(
                Column('name', css_class='form-group col-sm-6 col-12 mb-0 pb-0'),
                Column('servings', css_class='form-group col-sm-3 col-12 mb-0 pb-0'),
                Column('pax_serving', css_class='form-group col-sm-3 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('meal_categories', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-12 mb-0 pb-0'),
                Column('steps', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )


class MealUpateForm(forms.ModelForm):

    categories = MealCategory.objects.order_by('name').values_list('id', 'name')

    # meal_categories = forms.MultipleChoiceField(choices=list(categories), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Meal
        fields = ['image', 'name', 'servings', 'pax_serving', 'description', 'steps']

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
        tagged = Meal.objects.get(id=self.instance.id).meal_category
        if ',' in tagged:
            tagged = tagged.split(',')
        self.fields['meal_categories'].initial = tagged
        self.helper.layout = Layout(
            Row(
                Column('image', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('name', css_class='form-group col-sm-6 col-12 mb-0 pb-0'),
                Column('servings', css_class='form-group col-sm-3 col-12 mb-0 pb-0'),
                Column('pax_serving', css_class='form-group col-sm-3 col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('meal_categories', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-12 mb-0 pb-0'),
                Column('steps', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )
