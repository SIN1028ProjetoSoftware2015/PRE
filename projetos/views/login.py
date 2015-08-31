from django.contrib.auth import login, logout, authenticate, forms
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.urlresolvers import reverse
from projetos.utils import *

class LoginAdmin(TemplateView):
    template_name = 'projetos/login.html'


class PermissionDenied(TemplateView):
    template_name = 'projetos/home.html'

    def get_context_data(self, **kwargs):
        context = super(PermissionDenied, self).get_context_data(**kwargs)
        context['menu'] = ['home']
        messages.error(self.request, "Operação não permitida!")
        context = checkClient(self.request, context)
        return context


class PassAdmin(TemplateView):
    template_name = 'projetos/password.html'


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            if 'next' in request.GET and request.GET['next']!='' and '/login/' not in request.GET['next']:
                return HttpResponseRedirect(request.GET['next'])
            else:
                return HttpResponseRedirect(reverse('projetos:home'))
        else:
            messages.warning(request, "Usuário Inativo!")
            return HttpResponseRedirect(reverse('projetos:login'))
    else:
        messages.error(request, 'Usuário ou Senha inválido!')
        return HttpResponseRedirect(reverse('projetos:login'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('projetos:login'))