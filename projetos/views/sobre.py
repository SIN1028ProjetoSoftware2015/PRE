from django.views.generic import TemplateView
from projetos.models import Projeto, Participante

# Create your views here.
class SobreAdmin(TemplateView):
    template_name = 'projetos/sobre.html'

    def get_context_data(self, **kwargs):
        context = super(SobreAdmin, self).get_context_data(**kwargs)
        context['menu'] = 'sobre'
        context['total_participantes'] = Participante.objects.count()
        context['total_projetos'] = Projeto.objects.count()
        return context