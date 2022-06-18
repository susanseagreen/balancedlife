from __future__ import unicode_literals
from django.db import models
from app.registration.models import User


class Tracker(models.Model):
    code_user = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='code_user')
    name = models.CharField('Tracker Name', max_length=100)
    description = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Goal(models.Model):
    code_user = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='code_goal')
    name = models.CharField(max_length=30)
    colour = models.CharField(max_length=30)
    description = models.TextField(max_length=255, null=True, blank=True)


class TrackedItem(models.Model):
    code_tracker = models.ForeignKey(
        Tracker, on_delete=models.PROTECT,
        related_name='code_tracker_item')
    date = models.DateField('date')
    code_goal = models.ForeignKey(
        Goal, on_delete=models.PROTECT,
        related_name='code_tracker_item', null=True)
    description = models.TextField(max_length=255, null=True, blank=True)
