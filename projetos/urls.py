from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import home

urlpatterns = [
    url(r'^$', home.HomeAdmin.as_view(), name='apphome'),
]