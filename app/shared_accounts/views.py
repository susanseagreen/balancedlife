from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import SharedAccountCreateModalForm
from .models import SharedAccount


class SharedAccountModalCreateView(View):
    template_name = 'shared_accounts/shared_account_create_modal.html'

    def get(self, request, *args, **kwargs):

        form = SharedAccountCreateModalForm()

        shared_accounts = SharedAccount.objects.all()

        context = {
            'pk': kwargs['shopping_list_id'],
            'shared_accounts': shared_accounts,
            'form': form,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = SharedAccountCreateModalForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=True)
            instance.code_shopping_list_id = kwargs['shopping_list_id']
            instance.save()

        return redirect(self.request.META['HTTP_REFERER'])


class SharedAccountModalUpdateView(View):
    template_name = 'shared_accounts/shared_account_update_modal.html'

    def get(self, request, *args, **kwargs):

        shared_accounts = SharedAccount.objects.select_related('code_user').filter(code_shopping_list_id=kwargs['shopping_list_id'])

        context = {
            'shopping_list_id': kwargs['shopping_list_id'],
            'shared_accounts': shared_accounts,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        shared_accounts = SharedAccount.objects.filter(code_shopping_list_id=kwargs['shopping_list_id'])
        for shared_account in shared_accounts:
            if str(shared_account.id) in self.request.POST:
                shared_account.is_active = True
            else:
                shared_account.is_active = False
            shared_account.save()

        return redirect(self.request.META['HTTP_REFERER'])
