from django.views.generic import TemplateView
from projetos.models import Projeto, Participante, Unidade, ProjetoUnidade

class UnidadeAdmin(TemplateView):
	template_name = 'projetos/unidade.html'

	def get_context_data(self, **kwargs):
		context = super(UnidadeAdmin, self).get_context_data(**kwargs)

		context['menu'] = 'graficos'
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
		context['projeto_unidade'] = get_projeto_unidade(context['filtro_deps'])
		context['projeto_unidade_todos'] = get_projeto_unidade_todos()
		return context

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			request.POST._mutable = True
			params = {'params': dict((p, v) for p, v in request.POST.items() if v != None and len(v) > 0)}
			return self.render_to_response(self.get_context_data(**params))

def get_projeto_unidade(filtros):
	mapa = {}
	if filtros:
		for m in Unidade.objects.filter(codigo__in=filtros).order_by('nome'):
			mapa[m.nome] = {}
			mapa[m.nome]['count'] = ProjetoUnidade.objects.filter(unidade=m.codigo).count()
			mapa[m.nome]['id'] = m.codigo
	else:
		for m in Unidade.objects.all().order_by('nome'):
			mapa[m.nome] = {}
			mapa[m.nome]['count'] = ProjetoUnidade.objects.filter(unidade=m.codigo).count()
			mapa[m.nome]['id'] = m.codigo
	return mapa

def get_projeto_unidade_todos():
	mapa = {}
	for m in Unidade.objects.all():
		mapa[m.nome] = {}
		mapa[m.nome]['id'] = str(m.codigo)
	return mapa
