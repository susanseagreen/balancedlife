from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Ingredient, self).save(*args, **kwargs)
