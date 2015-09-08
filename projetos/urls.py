from django.conf.urls import url

from .views import home, reset_pass, sobre, projetos

urlpatterns = [
    url(r'^$', home.HomeAdmin.as_view(), name='home'),
    url(r'^sobre/', sobre.SobreAdmin.as_view(), name='sobre'),
    url(r'^listar/', projetos.ProjetosAdmin.as_view(), name='listar'),
]