from django.conf.urls import url

from . import views
from .views import ProductoActualizar, SedeActualizar, ClienteActualizar

app_name = 'compras'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compras/$', views.agregar_compra, name='agregar_compras'),
    url(r'^factura/$', views.manejar_factura, name='factura'),
    url(r'^pdffactura/$', views.pdf_factura, name='pdffactura'),
    url(r'^buscarfactura/$', views.buscar_factura, name='buscar_factura'),
    url(r'^buscarfacturapdf/$', views.buscar_factura_pdf, name='buscar_factura_pdf'),
    url(r'^mailfactura/$', views.pdf_reporte_semanal_view, name='mailfactura'),
    url(r'^agregarcliente/$', views.agregar_cliente, name='agregar_cliente'),
    url(r'^buscarclientes/$', views.buscar_cliente, name='buscar_cliente'),
    url(r'^clienteactualizar/(?P<pk>\d+)/$', ClienteActualizar.as_view(), name='actualizar_cliente'),
    url(r'^buscarproducto/$', views.buscar_producto, name='buscar_producto'),
    url(r'^agregarproductos/$', views.agregar_producto , name='agregar_producto'),
    url(r'^productoactualizar/(?P<pk>\d+)/$', ProductoActualizar.as_view(), name='actualizar_producto'),
    url(r'^buscarsede/$', views.buscar_sede , name='buscar_sede'),
    url(r'^agregarsedes/$', views.agregar_sede , name='agregar_sede'),
    url(r'^sedeactualizar/(?P<pk>\d+)/$', SedeActualizar.as_view(), name='actualizar_sede'),  
]