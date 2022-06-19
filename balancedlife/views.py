from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.tracker.models import Tracker, TrackedItem, Goal
from datetime import timedelta, datetime

three_months = 84


class HomeView(View):
    template_name = 'balancedlife_home.html'

    def get(self, request, *args, **kwargs):

        today = datetime.now().date()
        tracker_tables = {}
        goals = Goal.objects \
            .filter(code_user_id=self.request.user.pk) \
            .order_by("name")

        context = {
            "goals": goals,
            "today": today
        }

        trackers = Tracker.objects \
            .filter(code_user_id=self.request.user.pk) \
            .values("id", "name", "description", "created_at",
                    "code_tracker_item__id", "code_tracker_item__date",
                    "code_tracker_item__code_goal__name",
                    "code_tracker_item__code_goal__colour",
                    ).order_by("id", "code_tracker_item__date", "code_tracker_item__code_goal__colour")

        if trackers:
            tracker_id = ""
            for tracker in trackers:
                if "code_tracker_item__date" in tracker:
                    date = tracker["code_tracker_item__date"]
                    tracker_id = tracker["id"]

                    if "start_date" not in context:
                        if (today - tracker["code_tracker_item__date"]).days > three_months:
                            context["start_date"] = tracker["code_tracker_item__date"]
                        else:
                            if today.weekday() != 6:
                                context["start_date"] = (today - timedelta(today.weekday() + 1))
                            else:
                                context["start_date"] = today

                            context["end_date"] = date + timedelta(three_months - 1)

                    if (context["start_date"] - date).days <= three_months:

                        if tracker["id"] not in tracker_tables:
                            tracker_tables[tracker_id] = {
                                "created_at": tracker["created_at"],
                                "name": tracker["name"],
                                "description": tracker["description"],
                                "dates": {},
                            }

                        if date not in tracker_tables[tracker_id]["dates"]:
                            tracker_tables[tracker_id]["dates"][date] = []

                        if tracker["code_tracker_item__code_goal__colour"]:
                            tracker_tables[tracker_id]["dates"][date].append({
                                "name": tracker["code_tracker_item__code_goal__name"],
                                "colour": tracker["code_tracker_item__code_goal__colour"]
                            })

            dict_date = list(trackers)[-1]["code_tracker_item__date"]
            while dict_date != context["end_date"] and \
                    context["end_date"] >= dict_date:
                dict_date = dict_date + timedelta(1)
                if dict_date not in tracker_tables[tracker_id]["dates"]:
                    new_day = TrackedItem()
                    new_day.code_tracker_id = tracker_id
                    new_day.date = dict_date
                    new_day.save()
                    tracker_tables[tracker_id]["dates"][dict_date] = []

        context["tracker_tables"] = tracker_tables

        return render(request, template_name=self.template_name, context=context)
