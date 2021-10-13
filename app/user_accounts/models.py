from django.db import models


class UserAccountName(models.Model):
    is_active = models.BooleanField('Active', default=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserAccount(models.Model):
    is_active = models.BooleanField('Active', default=True)
    code_user_account = models.ForeignKey(UserAccountName, on_delete=models.PROTECT, default=1,
                                          related_name='user_account')
    code_user = models.ForeignKey('registration.User', on_delete=models.PROTECT, default=1,
                                  related_name='user_account')
    bool_main_user = models.BooleanField('Main User', default=False)
    bool_permissions = models.BooleanField('Permissions', default=False)

    def __str__(self):
        return self.code_user.username
