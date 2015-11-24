from django.views.generic import TemplateView
from projetos.models import Projeto, Participante, ProjetoParticipante, Unidade, ProjetoUnidade, Departamento
from projetos import utils
import datetime

# Create your views here.
class DepartamentoAdmin(TemplateView):
	template_name = 'projetos/departamento.html'

	def get_context_data(self, **kwargs):
		context = super(DepartamentoAdmin, self).get_context_data(**kwargs)
		context['menu'] = 'departamento'
		context['total_participantes'] = Participante.objects.count()
		context['total_projetos'] = Projeto.objects.count()
		filtros = None
		context['filtro_deps'] = None
		if 'params' in kwargs:
			filtros = kwargs['params']
		if filtros!=None and len(filtros)>0:
			context['filtro_deps'] = []
			for k, v in filtros.items():
				if 'csrfmiddlewaretoken' not in k:
					context['filtro_deps'].append(k)
		context['legend_template'] = "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
		context['projeto_unidade'] = get_projeto_unidade()
		context['participante_unidade'] = get_participante_unidade()
		context['projeto_departamento'] = get_projeto_departamento(context['filtro_deps'])
		context['projeto_departamento_todos'] = get_projeto_departamento_todos()
		return context

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			request.POST._mutable = True
			params = {'params': dict((p, v) for p, v in request.POST.items() if v != None and len(v) > 0)}
			return self.render_to_response(self.get_context_data(**params))

def get_projeto_departamento(filtros):
	mapa = {}
	if filtros:
		for m in Departamento.objects.filter(codigo__in=filtros).order_by('nome'):
			mapa[m.nome] = {}
			mapa[m.nome]['count'] = Projeto.objects.filter(departamento_id=m.codigo).count()
			mapa[m.nome]['id'] = m.codigo
	else:
		for m in Departamento.objects.all().order_by('nome'):
			mapa[m.nome] = {}
			mapa[m.nome]['count'] = Projeto.objects.filter(departamento_id=m.codigo).count()
			mapa[m.nome]['id'] = m.codigo
	return mapa

def get_projeto_departamento_todos():
	mapa = {}
	for m in Departamento.objects.all():
		mapa[m.nome] = {}
		mapa[m.nome]['id'] = str(m.codigo)
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
