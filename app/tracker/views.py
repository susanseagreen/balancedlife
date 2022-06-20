from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from app.tracker.models import Tracker, TrackedItem, Goal
from .forms import TrackerForm, GoalForm, AchievementForm
from datetime import datetime, timedelta


class TrackerAddView(View):
    template_name = 'tracker/add.html'

    def get(self, request, *args, **kwargs):

        form = TrackerForm()

        context = {
            'form': form,
        }

        # trackers = Tracker.objects.filter(code_user=self.request.user.pk)
        # if trackers:
        #     context["trackers"] = trackers

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = TrackerForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.code_user_id = self.request.user.pk
            if not instance.name:
                instance.name = "Daily Tracker"
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
            messages.success(self.request, f"New Daily Tracker Calendar created")

        return redirect(reverse_lazy('home'))


class TrackerUpdateView(View):
    template_name = 'tracker/update.html'

    def get(self, request, *args, **kwargs):
        tracker = Tracker.objects.get(id=kwargs["pk"])
        form = TrackerForm(instance=tracker)

        context = {
            'pk': kwargs["pk"],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        tracker = Tracker.objects.get(id=kwargs["pk"])
        form = TrackerForm(request.POST, instance=tracker)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.code_user_id = self.request.user.pk
            if not instance.name:
                instance.name = "Daily Tracker"
            instance.save()
            messages.success(self.request, f"Daily Tracker Calendar updated")

        return redirect(reverse_lazy('home'))


class TrackerDeleteView(View):
    template_name = 'tracker/delete.html'

    def get(self, request, *args, **kwargs):
        tracker = Tracker.objects \
            .get(id=kwargs["pk"])
        context = {"pk": kwargs["pk"], "tracker": tracker}

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        TrackedItem.objects.filter(code_tracker_id=self.kwargs['pk']).delete()
        Tracker.objects.get(id=self.kwargs['pk']).delete()
        messages.success(self.request, "Tracker deleted")

        return redirect(reverse_lazy('home'))


class GoalAddView(View):
    template_name = 'goal/add.html'

    def get(self, request, *args, **kwargs):
        goals = Goal.objects \
            .filter(code_user_id=self.request.user.pk) \
            .order_by("name")

        form = GoalForm()

        context = {
            'form': form,
            'goals': goals,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = instance.name.title()
            instance.code_user_id = self.request.user.pk
            instance.save()
            messages.success(self.request, f"Goal {instance.name} created")

        return redirect(self.request.META['HTTP_REFERER'])


class GoalUpdateView(View):
    template_name = 'goal/update.html'

    def get(self, request, *args, **kwargs):
        goal = Goal.objects \
            .get(id=kwargs["pk"])
        form = GoalForm(instance=goal)
        context = {"pk": kwargs["pk"], "form": form, "goal": goal}

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        goal = Goal.objects \
            .get(id=kwargs["pk"])
        form = GoalForm(request.POST, instance=goal)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(self.request, f"Goal {instance.name} updated")

        return redirect(reverse_lazy('home'))


class AchievementsView(View):
    template_name = 'achievement/list.html'

    def get(self, request, *args, **kwargs):
        goals = Goal.objects \
            .filter(code_user_id=self.request.user.pk) \
            .order_by("name")

        filters = {"user": self.request.user.id, "date": kwargs["date"]}
        form = AchievementForm(initial={'filters': filters})
        achievements = TrackedItem.objects \
            .filter(code_tracker_id=kwargs["tracker_id"], date=datetime.strptime(kwargs["date"], '%Y-%m-%d').date(),
                    code_goal__isnull=False) \
            .order_by("code_goal__colour") \
            .values("id", "code_goal__name", "code_goal__colour", "description")

        context = {
            'form': form,
            'tracker_id': kwargs["tracker_id"],
            'date': kwargs["date"],
            "goals": goals,
            "achievements": achievements
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = AchievementForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.code_tracker_id = kwargs["tracker_id"]
            instance.date = kwargs["date"]
            instance.save()
            messages.success(self.request, f"Achievement {instance.code_goal.name} created")

        return redirect(reverse_lazy('home'))


class AchievementUpdateView(View):
    template_name = 'achievement/update.html'

    def get(self, request, *args, **kwargs):
        achievement = TrackedItem.objects.get(id=kwargs["pk"])
        form = AchievementForm(instance=achievement)
        context = {"pk": kwargs["pk"], "form": form, "achievement": achievement}

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        achievement = TrackedItem.objects.get(id=kwargs["pk"])
        form = AchievementForm(request.POST, instance=achievement)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(self.request, f"Achievement {instance.code_goal.name} updated")

        return redirect(reverse_lazy('home'))


class AchievementDeleteView(View):
    template_name = 'achievement/delete.html'

    def get(self, request, *args, **kwargs):
        achievement = TrackedItem.objects \
            .get(id=kwargs["pk"])
        context = {"pk": kwargs["pk"], "achievement": achievement}

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        TrackedItem.objects.get(id=self.kwargs['pk']).delete()
        messages.success(self.request, "Achievement deleted")

        return redirect(reverse_lazy('home'))


class InsightsView(View):
    template_name = 'insights/list.html'

    def get(self, request, *args, **kwargs):
        insights = {}
        day_count = 1
        longest_streak = 0
        total_tracked = 0
        day = None

        tracked_items = TrackedItem.objects \
            .filter(code_tracker_id=kwargs["tracker_id"], code_goal__isnull=False, date__lte=datetime.now()) \
            .order_by("date", "code_goal_id") \
            .values("date", "description", "code_goal_id", "code_goal__name", "code_tracker__created_at",
                    "code_tracker__name")

        for tracked_item in tracked_items:
            goal_id = tracked_item["code_goal_id"]
            date = tracked_item["date"]
            if date >= tracked_item["code_tracker__created_at"]:
                if not insights:
                    day = date
                    insights = {
                        "name": tracked_item["code_tracker__name"],
                        "created": date,
                        "days": (datetime.now().date() - tracked_item["code_tracker__created_at"]).days + 1,
                        "date": {},
                        "goals": {}
                    }

                if date not in insights["date"]:
                    insights["date"][date] = []
                    total_tracked += 1
                if day != date:
                    day = date
                    day_count = 0
                day_count += 1
                day += timedelta(1)
                longest_streak = day_count if day_count > longest_streak else longest_streak

                if goal_id not in insights["goals"]:
                    insights["goals"][goal_id] = {"log_count": 0, "name": tracked_item["code_goal__name"]}
                insights["goals"][goal_id]["log_count"] += 1

                insights["date"][date].append({
                    "name": tracked_item["code_goal__name"],
                    "description": tracked_item["description"]
                })

        insights["longest_streak"] = longest_streak
        insights["total_tracked"] = total_tracked

        context = {"insights": insights, "tracked_items": tracked_items}

        return render(request, template_name=self.template_name, context=context)
