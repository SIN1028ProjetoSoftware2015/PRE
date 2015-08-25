from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from projetos.models import *
from datetime import datetime, timedelta
from django.http import HttpResponse
import json

# Create your views here.
class HomeAdmin(TemplateView):
    template_name = 'projetos/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeAdmin, self).get_context_data(**kwargs)
        context['menu'] = ['home']
        return context