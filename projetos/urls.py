from django.conf.urls import url


from .views import home, graficos, sobre, projetos, participantes, departamento,unidade,participante

from .views import home, graficos, sobre, projetos, participantes,unidade


urlpatterns = [
    url(r'^$', home.HomeAdmin.as_view(), name='home'),
    url(r'^sobre/', sobre.SobreAdmin.as_view(), name='sobre'),
    url(r'^participantes/detalhes', participantes.detalhes, name='participantes_detalhes'),
    url(r'^participantes/(?P<page>[0-9]+)/(?P<order>\w+)/(?P<tpOrder>\w+)/(?P<qtdPage>[0-9]+)',participantes.ParticipantesAdmin.as_view(), name='participantes'),
    url(r'^participantes/(?P<page>[0-9]+)/(?P<order>\w+)/(?P<tpOrder>\w+)', participantes.ParticipantesAdmin.as_view(), name='participantes'),
    url(r'^participantes/(?P<page>[0-9]+)', participantes.ParticipantesAdmin.as_view(), name='participantes'),
    url(r'^participantes/', participantes.ParticipantesAdmin.as_view(), name='participantes'),
    url(r'^projetos/detalhes', projetos.detalhes, name='projetos_detalhes'),
    url(r'^projetos/(?P<page>[0-9]+)/(?P<order>\w+)/(?P<tpOrder>\w+)/(?P<qtdPage>[0-9]+)', projetos.ProjetosAdmin.as_view(), name='projetos'),
    url(r'^projetos/(?P<page>[0-9]+)/(?P<order>\w+)/(?P<tpOrder>\w+)', projetos.ProjetosAdmin.as_view(), name='projetos'),
    url(r'^projetos/(?P<page>[0-9]+)', projetos.ProjetosAdmin.as_view(), name='projetos'),
    url(r'^projetos/', projetos.ProjetosAdmin.as_view(), name='projetos'),
    url(r'^graficos/', graficos.GraficosAdmin.as_view(), name='graficos'),

    url(r'^departamento/', departamento.DepartamentoAdmin.as_view(), name='departamento'),
    url(r'^unidade/', unidade.UnidadeAdmin.as_view(), name='unidade'),
    url(r'^participante/', participante.ParticipanteAdmin.as_view(), name='participante'),
   
    
    


]