from django.views.generic import TemplateView
from projetos.models import Projeto, Participante
from django.http import HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json
# Create your views here.
class ProjetosAdmin(TemplateView):
	template_name = 'projetos/projetos.html'

	def get_context_data(self, **kwargs):
		context = super(ProjetosAdmin, self).get_context_data(**kwargs)
		lista = Projeto.objects.all()
		context['menu'] = 'projetos'
		context['total_participantes'] = Participante.objects.count()
		context['total_projetos'] = len(lista)
		context['objetos'] = lista
		return context

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