from django.http import HttpResponse
from compras.models import Compras, Clientes, Log
from django.shortcuts import render, render_to_response, get_object_or_404, RequestContext
from django.db.models import Q
import datetime
#Se trae la serializacion
from django.core import serializers

# Create your views here.

def wsCompras_view(request):
    data = serializers.serialize("json",Compras.objects.all())
    return HttpResponse(data, content_type = 'application/json')

def wsComprasbyCliente_view(request):
    data = serializers.serialize("json",Compras.objects.filter(id_cliente = request.GET['cliente']))
    #Log
    Log.objects.create(fecha = datetime.datetime.now(), descripcion="Factura Generada JSON")
    return HttpResponse(data, content_type = 'application/json')

def buscar_factura_json(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(documento__icontains=query) |
            Q(nombres__icontains=query) 
        )
        results = Clientes.objects.filter(qset).distinct()
    else:
        results = []
    #Log
    Log.objects.create(fecha = datetime.datetime.now(), descripcion="Cliente Consultado")
    return render_to_response('wscompras/buscar_factura_json.html', {
        "results": results,
        "query": query
    }, context_instance = RequestContext(request))