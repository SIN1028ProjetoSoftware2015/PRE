from django.views.generic import TemplateView
from projetos.models import Projeto, Participante, ProjetoParticipante, Unidade, ProjetoUnidade
from projetos import utils
import datetime

# Create your views here.
class HomeAdmin(TemplateView):
	template_name = 'projetos/home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeAdmin, self).get_context_data(**kwargs)
		context['menu'] = 'home'
		context['total_participantes'] = Participante.objects.count()
		context['total_projetos'] = Projeto.objects.count()
		filtros = None
		if 'params' in kwargs:
			filtros = kwargs['params']
		if filtros!=None and len(filtros)>0:
			for k, v in filtros.items():
				if 'filter_year1' in k or 'filter_year' in k:
					context['filtro_nome'] = k
					context['filtro_valor'] = v
		context['legend_template'] = "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
		context['projeto_situacao'] = get_situacao_projetos(filtros)
		context['vinculo_participantes'] = get_vinculo_participantes(filtros)
		context['projeto_departamento'] = get_projeto_departamento()
		context['projeto_unidade'] = get_projeto_unidade()
		context['participante_unidade'] = get_participante_unidade()
		context['projetos_por_ano'] = get_projetos_por_ano(filtros)
		return context

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			request.POST._mutable = True
			params = {'params': dict((p, v) for p, v in request.POST.items() if v != None and len(v) > 0)}
			return self.render_to_response(self.get_context_data(**params))

def get_situacao_projetos(filtros):
	mapa = {}
	if filtros and 'filter_year' in filtros and filtros['filter_year'] != 'Todos':
		for m in Projeto.objects.order_by().values('situacao').distinct():
			mapa[m['situacao']] = Projeto.objects.filter(situacao=m['situacao'], data_registro__year=filtros['filter_year']).count()
			#print(Projeto.objects.filter(situacao=m['situacao'], data_registro__year=filtros['filter_year1']).query)
			
		
	else:
		for m in Projeto.objects.order_by().values('situacao').distinct():
			mapa[m['situacao']] = Projeto.objects.filter(situacao=m['situacao']).count()
			
	return mapa	

def get_projetos_por_ano(filtros):
	mapa = {}
	for m in Projeto.objects.order_by().values('data_conclusao').distinct():
		if 'data_conclusao' in m and m['data_conclusao'] != None and type(m['data_conclusao']) == datetime.datetime:
			if m['data_conclusao'].year in mapa:
				mapa[m['data_conclusao'].year] = mapa[m['data_conclusao'].year] + 1
			else:
				mapa[m['data_conclusao'].year] = 1

			
	return mapa
	


def get_vinculo_participantes(filtros):
	mapa = {}
	if filtros and 'filter_year' in filtros and filtros['filter_year'] != 'Todos':
		for m in ProjetoParticipante.objects.order_by().values('vinculo').distinct():
			mapa[m['vinculo']] = ProjetoParticipante.objects.filter(vinculo=m['vinculo'], data_inicial__year=filtros['filter_year']).values('participante').distinct().count()
	else:
		for m in ProjetoParticipante.objects.order_by().values('vinculo').distinct():
			mapa[m['vinculo']] = ProjetoParticipante.objects.filter(vinculo=m['vinculo']).count()
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
