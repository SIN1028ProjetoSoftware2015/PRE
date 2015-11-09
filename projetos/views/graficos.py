from django.views.generic import TemplateView
from projetos.models import Projeto, Participante, ProjetoParticipante, Unidade, ProjetoUnidade
from projetos import utils
import datetime

# Create your views here.
class GraficosAdmin(TemplateView):
	template_name = 'projetos/graficos.html'

	def get_context_data(self, **kwargs):
		context = super(GraficosAdmin, self).get_context_data(**kwargs)
		context['menu'] = 'graficos'
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
		context['projeto_departamento'] = get_projeto_departamento()
		context['projeto_unidade'] = get_projeto_unidade()
		context['participante_unidade'] = get_participante_unidade()
		return context

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			request.POST._mutable = True
			params = {'params': dict((p, v) for p, v in request.POST.items() if v != None and len(v) > 0)}
			return self.render_to_response(self.get_context_data(**params))

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
