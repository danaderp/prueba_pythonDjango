from django.conf.urls import url

from . import views

app_name = 'compras'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compras/$', views.compras, name='compras'),
    #url(r'^clientes/$', views.clientes , name='clientes'),
    url(r'^agregarcliente/$', views.agregar_cliente, name='agregar_cliente'),
    url(r'^buscarclientes/$', views.buscar_cliente, name='buscar_cliente'),
    url(r'^buscarproducto/$', views.buscar_producto, name='buscar_producto'),
    url(r'^agregarproductos/$', views.agregar_producto , name='agregar_producto'),
    url(r'^buscarsede/$', views.agregar_sede , name='buscar_sede'),
    url(r'^agregarsedes/$', views.buscar_sede , name='agregar_sede'),
    url(r'^sedes/$', views.sedes , name='sedes'),
]