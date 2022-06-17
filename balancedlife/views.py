from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(View):
    template_name = 'balancedlife_home.html'

    def get(self, request, *args, **kwargs):

        context = {}

        return render(request, template_name=self.template_name, context=context)
