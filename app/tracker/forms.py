from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Row, Column
from app.tracker.models import Tracker, Goal, TrackedItem

BLANK_CHOICE = (('', '---------'),)


class TrackerCreateForm(forms.ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = Tracker
        fields = ['name', 'description']


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'colour', 'description']

        widgets = {
            'colour': forms.TextInput(attrs={'type': 'color'}),
        }


class AchievementForm(forms.ModelForm):
    date = forms.CharField(required=False, widget=forms.TextInput(attrs={"readonly": True}))

    class Meta:
        model = TrackedItem
        fields = ['code_goal', 'description']
        labels = {
            'code_goal': 'Goal Achieved',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        filters = kwargs.get('initial', None)

        if filters:
            filters = kwargs['initial']['filters']
            goal = Goal.objects.filter(code_user_id=filters['user']).order_by("name").values_list("id", "name")
            self.fields['code_goal'].choices = BLANK_CHOICE + tuple(goal)
            self.fields['date'].initial = filters['date']

        self.helper.layout = Layout(
            Row(
                Column('code_goal', css_class='form-group col-12 col-md-8 mb-0 pb-0'),
                Column('date', css_class='form-group col-12 col-md-4 mb-0 pb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-12 mb-0 pb-0'),
                css_class='form-row'
            ),
        )
