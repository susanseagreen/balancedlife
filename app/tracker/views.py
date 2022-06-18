from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from app.tracker.models import Tracker, TrackedItem, Goal
from .forms import TrackerCreateForm, GoalCreateForm, AchievementCreateForm
from datetime import datetime, timedelta


class TrackerAddView(View):
    template_name = 'tracker/add.html'

    def get(self, request, *args, **kwargs):

        form = TrackerCreateForm()

        context = {
            'form': form,
        }

        trackers = Tracker.objects.filter(code_user=self.request.user.pk)
        if trackers:
            context["trackers"] = trackers

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = TrackerCreateForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.code_user_id = self.request.user.pk
            if not instance.name:
                instance.name = f"Tracker ({datetime.now().strftime('%d %b %Y')})"
            instance.save()

            if instance.created_at.weekday() != 6:
                sunday = instance.created_at - timedelta(instance.created_at.weekday() + 1)
            else:
                sunday = instance.created_at

            for day in range(0, 84):  # 3 months
                new_day = TrackedItem()
                new_day.code_tracker_id = instance.id
                new_day.date = sunday + timedelta(day)
                new_day.save()

        return redirect(reverse_lazy('home'))


class GoalAddView(View):
    template_name = 'goal/add.html'

    def get(self, request, *args, **kwargs):
        goals = Goal.objects \
            .filter(code_user_id=self.request.user.pk)

        form = GoalCreateForm()

        context = {
            'form': form,
            'goals': goals,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = GoalCreateForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = instance.name.title()
            instance.code_user_id = self.request.user.pk
            instance.save()

        return redirect(reverse_lazy('home'))


class AchievementsView(View):
    template_name = 'achievement/list.html'

    def get(self, request, *args, **kwargs):
        goals = Goal.objects \
            .filter(code_user_id=self.request.user.pk)

        filters = {"user": self.request.user.id}
        form = AchievementCreateForm(initial={'filters': filters})
        achievements = TrackedItem.objects \
            .filter(date=datetime.strptime(kwargs["date"], '%d %b %Y'), code_goal__isnull=False) \
            .order_by("code_goal__colour") \
            .values("code_goal__name", "code_goal__colour", "description")

        context = {
            'form': form,
            'tracker_id': kwargs["tracker_id"],
            'date': kwargs["date"],
            "goals": goals,
            "achievements": achievements
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = AchievementCreateForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.code_tracker_id = kwargs["tracker_id"]
            instance.date = datetime.strptime(kwargs["date"], '%d %b %Y')
            instance.save()

        return redirect(reverse_lazy('home'))
