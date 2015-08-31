from django.views.generic import TemplateView

# Create your views here.
class HomeAdmin(TemplateView):
    template_name = 'projetos/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeAdmin, self).get_context_data(**kwargs)
        context['menu'] = 'home'
        return context