from django.db import models


class MealCategory(models.Model):
    code_user_account = models.ForeignKey('user_accounts.UserAccountName', on_delete=models.PROTECT, default=1,
                                          related_name='meal_category')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
