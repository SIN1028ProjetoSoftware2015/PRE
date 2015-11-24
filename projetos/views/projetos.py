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
		context['filtro_campo'] = 'numero'
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
				print('Filtro: ', k, v)
				if 'numero' in k:
					context['filtro_nome'] = 'Número'
					context['filtro_campo'] = 'numero'
					context['filtro_valor'] = v
				elif 'titulo' in k:
					context['filtro_nome'] = 'Título'
					context['filtro_campo'] = 'titulo'
					context['filtro_valor'] = v
				elif 'situacao' in k:
					context['filtro_nome_situacao'] = 'Situação'
					context['filtro_valor_situacao'] = v
				elif 'data_inicial' in k:
					context['filtro_nome'] = 'Data Inicial'
					context['filtro_campo'] = 'data_inicial'
					context['filtro_valor'] = datetime.strptime(v.split(' ')[0], '%Y-%m-%d').strftime('%d/%m/%Y')
				elif 'data_conclusao' in k:
					context['filtro_nome'] = 'Data Conclusão'
					context['filtro_campo'] = 'data_conclusao'
					context['filtro_valor'] = datetime.strptime(v.split(' ')[0], '%Y-%m-%d').strftime('%d/%m/%Y')
				

		return paginar(kwargs, Projeto, 'numero', context, self.listFields, order_type='asc')

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			request.POST._mutable = True
			if 'data_inicial' in request.POST and len(request.POST.get('data_inicial')):
				try:
					data_inicial = datetime.strptime(request.POST['data_inicial'], '%d/%m/%Y')
					del request.POST['data_inicial']
					request.POST['data_inicial__gte'] = str(datetime.combine(data_inicial, time.min))
					request.POST['data_inicial__lte'] = str(datetime.combine(data_inicial, time.max))
				except:
					pass
			if 'data_conclusao' in request.POST and len(request.POST.get('data_conclusao')):
				try:
					data_final = datetime.strptime(request.POST['data_conclusao'], '%d/%m/%Y')
					del request.POST['data_conclusao']
					request.POST['data_conclusao__gte'] = str(datetime.combine(data_final, time.min))
					request.POST['data_conclusao__lte'] = str(datetime.combine(data_final, time.max))
				except:
					pass
			for p, v in request.POST.items():
				print(">>>>>> Parametro:", p, v)
			params = {'params': dict((p, v) for p, v in request.POST.items() if p.split('__')[0] in self.listFields and v != None and len(v) > 0)}
			return self.render_to_response(self.get_context_data(**params))



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