from django.urls import path
from app.tracker.views import TrackerAddView, GoalAddView, AchievementsView

app_name = "tracker"

urlpatterns = [
    path('add', TrackerAddView.as_view(), name='add'),
    path('goal/add', GoalAddView.as_view(), name='goal_add'),
    path('achievements/<tracker_id>/<date>', AchievementsView.as_view(), name='achievements'),
    # path('achievement/add', AchievementAddView.as_view(), name='achievement_add'),
]
