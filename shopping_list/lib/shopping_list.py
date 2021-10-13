from app.shopping_lists.models import ShoppingList


def build_shopping_lists(user_account_ids, user_account_choices):
    shopping_lists = ShoppingList.objects \
        .filter(code_user_account__in=user_account_ids) \
        .order_by('name', 'is_active')

    for shopping_list in shopping_lists:
        if shopping_list.code_user_account_id in user_account_choices:
            shopping_list.user_account_name = user_account_choices[shopping_list.code_user_account_id]['name']
            shopping_list.user_account_users = user_account_choices[shopping_list.code_user_account_id]['user']

    return shopping_lists
