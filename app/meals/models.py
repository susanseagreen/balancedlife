from django.db import models


class Meal(models.Model):
    name = models.CharField(max_length=50)
    image_link = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='default.png', blank=True)
    servings = models.IntegerField(default=1, blank=True, null=True)
    pax_serving = models.IntegerField("Pax per serving", default=2, blank=True, null=True)
    meal_category = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=True, blank=True)
    steps = models.TextField('Cooking Instructions', max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.pax_serving} pax / {self.servings} serving)"

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Meal, self).save(*args, **kwargs)
