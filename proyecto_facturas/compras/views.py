from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Clientes

# Create your views here.

def index(request):
    #template = loader.get_template('compras/index.html')
    #return HttpResponse("Hola mundo, esta es la pagina de Compras.")
     return render(request, 'compras/index.html')

def clientes(request):
    latest_clientes_list = Clientes.objects.order_by('-documento')[:5]
    template = loader.get_template('compras/clientes.html')
    context = {
        'latest_clientes_list': latest_clientes_list,
    }
    return HttpResponse(template.render(context, request))
    #output = ', '.join([q.nombres for q in latest_clientes_list])
    #return HttpResponse(output)

def productos(request):
    return HttpResponse("You're looking at Producto%s." )

def sedes(request):
    return HttpResponse("You're looking at Sedes%s." )

def compras(request, compra_id):
    return HttpResponse("You're looking at Compras%s." % compra_id)
