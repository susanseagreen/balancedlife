from app.user_accounts.models import UserAccount


def get_user_accounts(self):
    user_accounts = UserAccount.objects \
        .select_related('code_user', 'code_user_account', 'code_user_account__user_account',
                        'code_user_account__user_account__code_user') \
        .filter(code_user=self.request.user.id, is_active=True) \
        .values(
            'id', 'code_user_account_id',
            'code_user_account__name',
            'code_user_account__user_account__code_user__username',
        )

    return user_accounts


def build_lookup_dict(self, user_accounts):
    user_account_ids = []
    user_account_choices = {}
    for user_account in user_accounts:
        account_id = user_account['code_user_account_id']
        if account_id not in user_account_choices:
            user_account_ids.append(account_id)
            user_account_choices[account_id] = {}
            user_account_choices[account_id]['user'] = []
            user_account_choices[account_id]['name'] = user_account['code_user_account__name']
            user_account_choices[account_id]['names'] = 'You'
        username = user_account["code_user_account__user_account__code_user__username"]
        if username != self.request.user.username:
            user_account_choices[account_id]['names'] = user_account_choices[account_id]['names'] + f', {username}'
        user_account_choices[account_id]['user'].append(username)

    return user_account_ids, user_account_choices


def build_user_account_tuple(user_account_choices):
    user_account_tuple = []
    for user_account_choice in user_account_choices:
        account = user_account_choices[user_account_choice]
        user_account_tuple.append([user_account_choice, f"{account['name']} ({account['names']})"])

    return user_account_tuple
