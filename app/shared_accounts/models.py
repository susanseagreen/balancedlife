from django.db import models


class SharedAccount(models.Model):
    is_active = models.BooleanField('Active', default=True)
    code_user = models.ForeignKey('registration.User', on_delete=models.PROTECT, default=1,
                                  related_name='shared_accounts')
    code_shopping_list = models.ForeignKey('shopping_lists.ShoppingList', on_delete=models.PROTECT, default=1,
                                           related_name='shared_accounts')
