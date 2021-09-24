from django.db import models


class ShoppingList(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.username = self.name.title()
        return super(ShoppingList, self).save(*args, **kwargs)
