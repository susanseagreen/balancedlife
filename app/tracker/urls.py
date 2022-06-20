from django.urls import path
from app.tracker.views import (
    TrackerAddView, TrackerUpdateView, TrackerDeleteView,
    GoalAddView, GoalUpdateView,
    AchievementsView, AchievementUpdateView, AchievementDeleteView,
    InsightsView
)

app_name = "tracker"

urlpatterns = [
    path('add', TrackerAddView.as_view(), name='add'),
    path('update/<pk>', TrackerUpdateView.as_view(), name='update'),
    path('delete/<pk>', TrackerDeleteView.as_view(), name='delete'),
    path('goal/add', GoalAddView.as_view(), name='goal_add'),
    path('goal/update/<pk>', GoalUpdateView.as_view(), name='goal_update'),
    path('achievements/<tracker_id>/<date>', AchievementsView.as_view(), name='achievements'),
    path('achievement/update/<pk>', AchievementUpdateView.as_view(), name='achievement_update'),
    path('achievement/delete/<pk>', AchievementDeleteView.as_view(), name='achievement_delete'),
    path('insights/<tracker_id>', InsightsView.as_view(), name='insights'),
]
