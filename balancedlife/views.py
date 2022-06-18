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

        today = datetime.now()
        tracker_tables = {}
        goals = Goal.objects \
            .filter(code_user_id=self.request.user.pk)

        context = {
            "goals": goals,
            "today": today.strftime('%d %b %Y')
        }

        trackers = Tracker.objects \
            .filter(code_user_id=self.request.user.pk) \
            .values("id", "name", "description",
                    "code_tracker_item__id", "code_tracker_item__date",
                    "code_tracker_item__code_goal__name",
                    "code_tracker_item__code_goal__colour",
                    ).order_by("id", "code_tracker_item__date", "code_tracker_item__code_goal__colour")

        if trackers:
            tracker_id = ""
            tracker_name = ""
            for tracker in trackers:
                date = tracker["code_tracker_item__date"].strftime('%d %b %Y')
                tracker_id = tracker["id"]
                tracker_name = tracker["name"]

                if "start_date" not in context:
                    if today.weekday() != 6:
                        context["start_date"] = today - timedelta(today.weekday() + 1)
                    else:
                        context["start_date"] = today

                    context["end_date"] = (datetime.strptime(date, '%d %b %Y') +
                                           timedelta(three_months - 1)).strftime('%d %b %Y')

                if context["start_date"].strptime(date, '%d %b %Y') <= datetime.strptime(date, '%d %b %Y'):
                    if (today - datetime.strptime(date, '%d %b %Y')).days <= three_months:

                        if tracker["id"] not in tracker_tables:
                            tracker_tables[tracker_id] = {}
                            tracker_tables[tracker_id][tracker_name] = {}

                        if date not in tracker_tables[tracker_id][tracker_name]:
                            tracker_tables[tracker_id][tracker_name][date] = []

                        if tracker["code_tracker_item__code_goal__colour"]:
                            tracker_tables[tracker_id][tracker_name][date].append((
                                tracker["code_tracker_item__code_goal__name"],
                                tracker["code_tracker_item__code_goal__colour"]))

            dict_date = list(trackers)[-1]["code_tracker_item__date"]
            while dict_date.strftime('%d %b %Y') != context["end_date"] and \
                    datetime.strptime(context["end_date"], '%d %b %Y') >= \
                    datetime.strptime(dict_date.strftime('%d %b %Y'), '%d %b %Y'):
                dict_date = dict_date + timedelta(1)
                if dict_date not in tracker_tables[tracker_id][tracker_name]:
                    new_day = TrackedItem()
                    new_day.code_tracker_id = tracker_id
                    new_day.date = dict_date
                    new_day.save()
                    tracker_tables[tracker_id][tracker_name][dict_date] = []

        context["tracker_tables"] = tracker_tables

        return render(request, template_name=self.template_name, context=context)
