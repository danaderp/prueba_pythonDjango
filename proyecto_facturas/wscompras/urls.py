from django.conf.urls import url
from . import views

app_name = 'wscompras'

urlpatterns = [
    url(r'^wscompras/$', views.wsCompras_view, name='wscompras'),
    url(r'^generarjson/$', views.wsComprasbyCliente_view, name='generar_json'),
    url(r'^buscarfacturajson/$', views.buscar_factura_json, name='buscar_factura_json'),
]