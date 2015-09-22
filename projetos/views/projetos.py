from django.views.generic import TemplateView
from projetos.models import Projeto, Participante
from django.http import HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from projetos.utils import paginar
from datetime import datetime, time, timedelta
import json

filtros = None

# Create your views here.
class ProjetosAdmin(TemplateView):
	template_name = 'projetos/projetos.html'
	listFields = sorted([x for x, y in Projeto().__dict__.items() if not x.startswith('_')])

	def get_context_data(self, **kwargs):
		global filtros
		context = super(ProjetosAdmin, self).get_context_data(**kwargs)
		context['menu'] = 'projetos'
		context['total_participantes'] = Participante.objects.count()
		context['total_projetos'] = Projeto.objects.count()
		context['filtro_nome'] = 'Número'
		context['filtro_valor'] = ''
		if 'params' in kwargs:
			filtros = kwargs['params']
		elif 'page' in kwargs and filtros != None:
			kwargs['params'] = filtros
		elif 'params' not in kwargs:
			filtros = None
		if 'params' not in kwargs:
			kwargs['params'] = {}

		return paginar(kwargs, Projeto, 'numero', context, self.listFields, order_type='asc')



def detalhes(request):
	if request.method == 'POST':
		try:
			detalhes_result = Projeto.objects.filter(numero=request.POST['numero'])
			if len(detalhes_result) >= 1:
				detalhes_items = serializers.serialize('json', detalhes_result)
				tmp = json.loads(detalhes_items)
				result = json.dumps(tmp)
		except ObjectDoesNotExist:
			result = json.dumps({'resultFail':'Nenhuma informação de Projetos para exibir.'})
		return HttpResponse(result)
	else:
		return HttpResponse(json.dumps({'resultFail':'Nenhuma informação de Projetos para exibir.'}), content_type="application/json")