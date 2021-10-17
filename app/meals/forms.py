from django import forms
from app.meals.models import Meal
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Fieldset
from app.meal_categories.models import MealCategory


class MealCreateForm(forms.ModelForm):

    meal_categories = forms.MultipleChoiceField(choices='', widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Meal
        fields = ['image_link', 'image', 'name', 'servings', 'pax_serving', 'description', 'steps']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'steps': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'image_link': 'Image URL',
            'image': 'Image Upload',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        categories = MealCategory.objects.order_by('name').values_list('id', 'name')
        self.fields['meal_categories'].choices = list(categories)
        self.helper.layout = Layout(
            Row(
                Column('image_link', css_class='form-group col-12 mb-0 pb-0'),
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


class MealUpdateForm(forms.ModelForm):

    meal_categories = forms.MultipleChoiceField(choices='', widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Meal
        fields = ['image_link', 'image', 'name', 'servings', 'pax_serving', 'description', 'steps']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'steps': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'image_link': 'Image URL',
            'image': 'Image Upload',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        tagged = Meal.objects.get(id=self.instance.id).meal_category
        if ',' in tagged:
            tagged = tagged.split(',')
        categories = MealCategory.objects.order_by('name').values_list('id', 'name')
        self.fields['meal_categories'].initial = tagged
        self.fields['meal_categories'].choices = list(categories)
        self.helper.layout = Layout(
            Row(
                Column('image_link', css_class='form-group col-12 mb-0 pb-0'),
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