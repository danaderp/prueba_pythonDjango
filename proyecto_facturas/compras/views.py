from django.forms import modelformset_factory
from django.shortcuts import render, render_to_response, get_object_or_404, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.forms import modelform_factory
from django.db.models import Q
from .models import Clientes, Productos, Sedes, Compras
from .forms import ClienteForm, ProductoForm, SedeForm, CompraForm, CompraFormSet
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError 

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
    
def buscar_factura(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(documento__icontains=query) |
            Q(nombres__icontains=query) 
        )
        results = Clientes.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('compras/buscar_factura.html', {
        "results": results,
        "query": query
    }, context_instance = RequestContext(request))

def manejar_factura(request):
    cliente = Clientes.objects.get(pk=request.GET['cliente'])
    #qset = Compras.objects.filter(id_cliente = request.GET['cliente'])
    #qset = Compras.objects.all()
    #formset = CompraFormSet(queryset = qset)
    if request.method == "POST":
        formset = CompraFormSet(request.POST, request.FILES, instance=cliente)
        if formset.is_valid():
            formset.save()
        return HttpResponseRedirect('/compras/')

    else:
        formset = CompraFormSet(instance=cliente)
    return render(request,'compras/manejar_factura.html', {'formset': formset, 'cliente':cliente})



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


def agregar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/compras/buscarfactura/')
    else:
        form = CompraForm()
    return render(request, 'compras/agregar_compra.html', {'form': form})
