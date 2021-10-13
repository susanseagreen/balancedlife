from django.db import models


class ShoppingList(models.Model):
    code_user_account = models.ForeignKey('user_accounts.UserAccountName', on_delete=models.PROTECT, default=1,
                                          related_name='shopping_list')
    is_active = models.BooleanField('Active', default=True)
    name = models.CharField(max_length=50)
    date_from = models.DateTimeField('date from', blank=True, null=True)
    date_to = models.DateTimeField('date to', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(ShoppingList, self).save(*args, **kwargs)
