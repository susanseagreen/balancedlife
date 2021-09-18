from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    steps = models.TextField('Cooking Instructions', max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name
