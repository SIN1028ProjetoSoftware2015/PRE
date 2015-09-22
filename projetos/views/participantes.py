from django.views.generic import TemplateView
from projetos.models import Projeto, Participante, ProjetoParticipante
from django.http import HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json
from projetos.utils import paginar

filtros = None

# Create your views here.
class ParticipantesAdmin(TemplateView):
	template_name = 'projetos/participantes.html'
	listFields = sorted([x for x, y in Participante().__dict__.items() if not x.startswith('_')])
	listFields.append('unidade')

	def get_context_data(self, **kwargs):
		global filtros
		context = super(ParticipantesAdmin, self).get_context_data(**kwargs)
		context['menu'] = 'participantes'
		context['total_participantes'] = Participante.objects.count()
		context['total_projetos'] = Projeto.objects.count()
		context['filtro_nome'] = 'Matrícula'
		context['filtro_valor'] = ''
		if 'params' in kwargs:
			filtros = kwargs['params']
		elif 'page' in kwargs and filtros != None:
			kwargs['params'] = filtros
		elif 'params' not in kwargs:
			filtros = None
		if 'params' not in kwargs:
			kwargs['params'] = {}
		if filtros!=None and len(filtros)>0:
			for k, v in filtros.items():
				if 'matricula' in k:
					context['filtro_nome'] = 'Matrícula'
					context['filtro_valor'] = v
				elif 'nome' in k and 'unidade' not in k:
					context['filtro_nome'] = 'Nome'
					context['filtro_valor'] = v
				elif 'unidade' in k:
					context['filtro_nome'] = 'Unidade'
					context['filtro_valor'] = v
		return paginar(kwargs, Participante, 'matricula', context, self.listFields, lista_fetch=['unidade'], order_type='asc')

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			request.POST._mutable = True
			if 'unidade_nome' in request.POST and len(request.POST.get('unidade_nome')):
				request.POST['unidade__nome__icontains'] = request.POST['unidade_nome']
				del request.POST['unidade_nome']
			params = {'params': dict((p, v) for p, v in request.POST.items() if p.split('__')[0] in self.listFields and v != None and len(v) > 0)}
			return self.render_to_response(self.get_context_data(**params))

def detalhes(request):
	if request.method == 'POST':
		try:
			detalhes_result = ProjetoParticipante.objects.filter(participante__matricula=request.POST['matricula'])
			if len(detalhes_result) > 0:
				detalhes_items = serializers.serialize('json', detalhes_result)
				tmp = json.loads(detalhes_items)
				for x in tmp:
					x['fields']['projeto_nome'] = Projeto.objects.get(pk=x['fields']['projeto']).titulo
				result = json.dumps(tmp)
			else:
				result = json.dumps({'resultFail':'Nenhuma informação de Projetos para exibir.'})
		except ObjectDoesNotExist:
			result = json.dumps({'resultFail':'Nenhuma informação de Projetos para exibir.'})
		return HttpResponse(result)
	else:
		return HttpResponse(json.dumps({'resultFail':'Nenhuma informação de Projetos para exibir.'}), content_type="application/json")