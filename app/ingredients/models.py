from django.db import models
from common.choices import food_group_choices


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    food_group = models.CharField(choices=food_group_choices, default="", max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
