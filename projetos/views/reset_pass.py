from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from projetos.forms import PasswordResetForm
from projetos.utils import *

def reset(request):
    UserModel = get_user_model()
    if 'username' in request.POST:
        request.POST._mutable = True
        try:
            usuario = UserModel.objects.get(username=request.POST['username'])
            request.POST['email'] = usuario.email
            messages.success(request, 'Um e-email foi enviado para %s com a redefinição de senha!' % usuario.email)
        except:
            messages.error(request, 'E-mail não cadastrado na aplicação!')
            return HttpResponseRedirect(reverse('projetos:reset'))
    return password_reset(request, template_name='projetos/registro/reset.html', email_template_name='projetos/registro/reset_email.html',
        html_email_template_name='projetos/registro/reset_email.html', subject_template_name='projetos/registro/reset_subject.txt',
        post_reset_redirect=reverse('projetos:success'), password_reset_form=PasswordResetForm)


def reset_confirm(request, uidb64=None, token=None):
    if 'new_password1' in request.POST and 'new_password2' in request.POST:
        if request.POST['new_password1'] != request.POST['new_password2']:
            messages.error(request, 'Senha difere da confirmação de senha!')
            return HttpResponseRedirect(request.path)
        else:
            r = checkPaswStrength(request.POST['new_password1'], settings.TAMANHO_MINIMO_SENHA)
            if r!=True:
                messages.warning(request, str(r))
                return HttpResponseRedirect(request.path)
    x = password_reset_confirm(request, template_name='projetos/registro/reset_confirm.html', uidb64=uidb64, token=token, post_reset_redirect=reverse('projetos:success'))
    if hasattr(x, 'url') and x.url == '/success/':
        messages.success(request, 'Sua senha foi definida com sucesso!')
    return x


def success(request):
    return HttpResponseRedirect(reverse('projetos:login'))