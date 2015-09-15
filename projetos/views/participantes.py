from django.views.generic import TemplateView
from projetos.models import Projeto, Participante, ProjetoParticipante
from django.http import HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json

# Create your views here.
class ParticipantesAdmin(TemplateView):
	template_name = 'projetos/participantes.html'

	def get_context_data(self, **kwargs):
		context = super(ParticipantesAdmin, self).get_context_data(**kwargs)
		lista = Participante.objects.all()
		context['menu'] = 'participantes'
		context['total_participantes'] = len(lista)
		context['total_projetos'] = Projeto.objects.count()
		context['objetos'] = lista
		return context

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