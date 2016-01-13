from django.forms import modelformset_factory
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.forms import modelform_factory
from django.db.models import Q
from .models import Clientes, Productos, Sedes
from .forms import ClienteForm, ProductoForm, SedeForm

# Create your views here.

def index(request):
    #template = loader.get_template('compras/index.html')
    #return HttpResponse("Hola mundo, esta es la pagina de Compras.")
     return render(request, 'compras/index.html')

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/compras/buscarclientes/')
    else:
        form = ClienteForm()
    return render(request,'compras/agregar_cliente.html', {'form': form})
    #output = ', '.join([q.nombres for q in latest_clientes_list])
    #return HttpResponse(output)

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/compras/buscarproducto/')
    else:
        form = ProductoForm()
    return render(request,'compras/agregar_producto.html', {'form': form})

def agregar_sede(request):
    if request.method == 'POST':
        form = SedeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/compras/buscarsede/')
    else:
        form = SedeForm()
    return render(request,'compras/agregar_sede.html', {'form': form})

def buscar_cliente(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(documento__icontains=query) |
            Q(nombres__icontains=query) 
        )
        results = Clientes.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('compras/buscar_cliente.html', {
        "results": results,
        "query": query
    })

def manage_clientes(request):
    ClienteFormSet = modelformset_factory(Clientes, fields =('documento','nombres','detalles'))
    if request.method == 'POST':
        formset = ClienteFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('compras/index.html')
    else:
        formset = ClienteFormSet()
    return render(request, 'compras/manage_clientes.html', {'formset': formset})



def buscar_producto(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(producto__icontains=query) |
            Q(descripcion__icontains=query) 
        )
        results = Productos.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('compras/buscar_producto.html', {
        "results": results,
        "query": query
    })

def buscar_sede(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(sede__icontains=query) |
            Q(direccion__icontains=query) 
        )
        results = Sedes.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('compras/buscar_sede.html', {
        "results": results,
        "query": query
    })

def sedes(request):
    return HttpResponse("You're looking at Sedes%s." )

#def compras(request, compra_id):
 #   return HttpResponse("You're looking at Compras%s." % compra_id)


def compras(request):
    return render(request, 'compras/compras.html')
