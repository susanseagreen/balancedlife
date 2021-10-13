from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import UserAccountCreateModalForm, UserAccountUpdateModalForm
from .models import UserAccount
from app.registration.models import User
from app.shopping_lists.models import ShoppingList
from .lib import user_accounts


class UserAccountModalCreateView(View):
    template_name = 'user_accounts/user_account_create_modal.html'

    def get(self, request, *args, **kwargs):

        shopping_list = ShoppingList.objects.get(id=kwargs['shopping_list_id'])
        user_list = User.objects.exclude(user_account__code_user_account_id=shopping_list.code_user_account.id, is_active=True)

        filters = {
            'user': user_list,
        }
        form = UserAccountCreateModalForm(initial={'filters': filters})

        users = User.objects.filter(user_account__code_user_account_id=shopping_list.code_user_account.id, is_active=True)

        context = {
            'shopping_list_id': kwargs['shopping_list_id'],
            'shopping_list': shopping_list,
            'user_list': user_list,
            'users': users,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = UserAccountCreateModalForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.code_shopping_list_id = kwargs['shopping_list_id']
            instance.save()

        return redirect(self.request.META['HTTP_REFERER'])


class UserAccountModalUpdateView(View):
    template_name = 'user_accounts/user_account_update_modal.html'

    def get(self, request, *args, **kwargs):

        user_accounts_list = user_accounts.get_user_accounts(self)
        user_account_ids, user_account_choices = user_accounts.build_lookup_dict(self, user_accounts_list)
        user_account_tuple = user_accounts.build_user_account_tuple(user_account_choices)

        shopping_list = ShoppingList.objects.get(id=self.kwargs['shopping_list_id'])

        filters = {
            'user_account_tuple': user_account_tuple,
            'user_account_id': shopping_list.code_user_account_id,
        }

        form = UserAccountUpdateModalForm(initial={'filters': filters})

        context = {
            'shopping_list_id': self.kwargs['shopping_list_id'],
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)\

    def post(self, request, *args, **kwargs):

        user_accounts = UserAccount.objects.filter(code_shopping_list_id=kwargs['shopping_list_id'])
        for user_account in user_accounts:
            if str(user_account.id) in self.request.POST:
                user_account.is_active = True
            else:
                user_account.is_active = False
            user_account.save()

        return redirect(self.request.META['HTTP_REFERER'])
