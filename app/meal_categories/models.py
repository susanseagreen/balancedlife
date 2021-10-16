from django.db import models


class MealCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(MealCategory, self).save(*args, **kwargs)
