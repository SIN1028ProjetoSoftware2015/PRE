from django.views.generic import TemplateView
from projetos.models import Projeto, Participante, ProjetoParticipante, Unidade, ProjetoUnidade
from projetos import utils

# Create your views here.
class HomeAdmin(TemplateView):
    template_name = 'projetos/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeAdmin, self).get_context_data(**kwargs)
        context['menu'] = 'home'
        context['total_participantes'] = Participante.objects.count()
        context['total_projetos'] = Projeto.objects.count()
        context['legend_template'] = "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
        context['projeto_situacao'] = get_situacao_projetos()
        context['vinculo_participantes'] = get_vinculo_participantes()
        context['projeto_departamento'] = get_projeto_departamento()
        context['projeto_unidade'] = get_projeto_unidade()
        context['participante_unidade'] = get_participante_unidade()
        return context


def get_situacao_projetos():
	mapa = {}
	for m in Projeto.objects.order_by().values('situacao').distinct():
		mapa[m['situacao']] = Projeto.objects.filter(situacao=m['situacao']).count()
	return mapa


def get_vinculo_participantes():
	mapa = {}
	for m in ProjetoParticipante.objects.order_by().values('vinculo').distinct():
		mapa[m['vinculo']] = ProjetoParticipante.objects.filter(vinculo=m['vinculo']).values('participante').distinct().count()
	return mapa

def get_projeto_departamento():
	mapa = {}
	for m in Projeto.objects.order_by().values('departamento').distinct():
		mapa[m['departamento']] = Projeto.objects.filter(departamento=m['departamento']).count()
	return mapa

def get_projeto_unidade():
	mapa = {}
	for m in Unidade.objects.all():
		mapa[m.nome] = ProjetoUnidade.objects.filter(unidade=m.codigo).count()
	return mapa

def get_participante_unidade():
	mapa = {}
	for m in Unidade.objects.all():
		mapa[m.nome] = Participante.objects.filter(unidade=m.codigo).count()
	return mapa
