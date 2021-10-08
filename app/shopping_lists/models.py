from django.db import models
from django.contrib.auth import get_user_model


class ShoppingList(models.Model):
    code_user = models.ForeignKey('registration.User', on_delete=models.PROTECT, default=1, related_name='shopping_list')
    name = models.CharField(max_length=50)
    date_from = models.DateTimeField('date from', blank=True, null=True)
    date_to = models.DateTimeField('date to', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(ShoppingList, self).save(*args, **kwargs)
