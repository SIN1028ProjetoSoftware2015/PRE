from django.views.generic import TemplateView

# Create your views here.
class SobreAdmin(TemplateView):
    template_name = 'projetos/sobre.html'

    def get_context_data(self, **kwargs):
        context = super(SobreAdmin, self).get_context_data(**kwargs)
        context['menu'] = 'sobre'
        return context