from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import home, login, reset_pass, sobre

urlpatterns = [
    url(r'^$', login_required(home.HomeAdmin.as_view()), name='home'),
    url(r'^sobre/', login_required(sobre.SobreAdmin.as_view()), name='sobre'),
    url(r'^auth/', login.login_view, name='auth'),
    url(r'^login/', login.LoginAdmin.as_view(), name='login'),
    url(r'^logout/', login.logout_view, name='logout'),
    url(r'^passwd/', login.PassAdmin.as_view(), name='password'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', reset_pass.reset_confirm, name='password_reset_confirm'),
    url(r'^reset/$', reset_pass.reset, name='reset'),
    url(r'^success/$', reset_pass.success, name='success'),
]