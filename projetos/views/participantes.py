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
		if 'params' in kwargs:
			filtros = kwargs['params']
		elif 'page' in kwargs and filtros != None:
			kwargs['params'] = filtros
		elif 'params' not in kwargs:
			filtros = None
		if 'params' not in kwargs:
			kwargs['params'] = {}
		
		return paginar(kwargs, Participante, 'matricula', context, self.listFields, lista_fetch=['unidade'], order_type='asc')


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