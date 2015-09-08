from django.views.generic import TemplateView
from projetos.models import Projeto

# Create your views here.
class ProjetosAdmin(TemplateView):
    template_name = 'projetos/projetos.html'

    def get_context_data(self, **kwargs):
        context = super(ProjetosAdmin, self).get_context_data(**kwargs)
        lista = Projeto.objects.all()
        context['menu'] = 'projetos'
        context['objetos'] = lista
        return context