from django.conf.urls import url

from . import views

app_name = 'compras'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^clientes/$', views.clientes , name='clientes'),
    url(r'^productos/$', views.productos , name='productos'),
    url(r'^sedes/$', views.sedes , name='sedes'),
]