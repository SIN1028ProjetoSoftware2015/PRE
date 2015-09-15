from django.conf.urls import url

from .views import home, sobre, projetos, participantes

urlpatterns = [
    url(r'^$', home.HomeAdmin.as_view(), name='home'),
    url(r'^sobre/', sobre.SobreAdmin.as_view(), name='sobre'),
    url(r'^participantes/detalhes', participantes.detalhes, name='participantes_detalhes'),
    url(r'^participantes/', participantes.ParticipantesAdmin.as_view(), name='participantes'),
    url(r'^projetos/detalhes', projetos.detalhes, name='projetos_detalhes'),
    url(r'^projetos/', projetos.ProjetosAdmin.as_view(), name='projetos'),
]