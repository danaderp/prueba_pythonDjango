from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .models import Clientes, Productos, Sedes, Compras, Log
from .forms import ClienteForm, ProductoForm, SedeForm, CompraForm, CompraFormSet
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
import datetime
from django.db.models import Sum, Avg, Max, Min, Count
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, Table, TableStyle
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


# Create your views here.

def index(request):
    #template = loader.get_template('compras/index.html')
    #return HttpResponse("Hola mundo, esta es la pagina de Compras.")
     actualizacion = Log.objects.all().order_by('fecha').reverse()[:6]
     return render(request, 'compras/index.html', {'actualizacion':actualizacion})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            #Log
            Log.objects.create(fecha = datetime.datetime.now(), descripcion="Cliente Agregado")
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
            #Log
            Log.objects.create(fecha = datetime.datetime.now(), descripcion="Producto Agregado")
            return HttpResponseRedirect('/compras/buscarproducto/')
    else:
        form = ProductoForm()
    return render(request,'compras/agregar_producto.html', {'form': form})

def agregar_sede(request):
    if request.method == 'POST':
        form = SedeForm(request.POST)
        if form.is_valid():
            form.save()
            #Log
            Log.objects.create(fecha = datetime.datetime.now(), descripcion="Sede Agregada")
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
    #Log
    Log.objects.create(fecha = datetime.datetime.now(), descripcion="Cliente Consultado")
    
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
    #Log
    Log.objects.create(fecha = datetime.datetime.now(), descripcion="Factura Consultada")
    return render_to_response('compras/buscar_factura.html', {
        "results": results,
        "query": query
    }, context_instance = RequestContext(request))

def buscar_factura_pdf(request):
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
    Log.objects.create(fecha = datetime.datetime.now(), descripcion="Factura Consultada PDF")
    
    return render_to_response('compras/buscar_factura_pdf.html', {
        "results": results,
        "query": query
    }, context_instance = RequestContext(request))

def manejar_factura(request):
    cliente = Clientes.objects.get(pk=request.GET['cliente'])
    
    if request.method == "POST":
        formset = CompraFormSet(request.POST, request.FILES, instance=cliente)
        if formset.is_valid():
            formset.save()
            #Log
            Log.objects.create(fecha = datetime.datetime.now(), descripcion="Factura Actualizada")
        return HttpResponseRedirect('/compras/')

    else:
        formset = CompraFormSet(instance=cliente)
        #Se trae el precio de producto si las compras no lo registran
        comprasByCliente = Compras.objects.filter(id_cliente = request.GET['cliente']).filter(
                    precio = None).order_by('id_producto').values_list('id_producto',flat=True)
        productosByCompras = Productos.objects.filter(id__in = list(comprasByCliente))
        
        for p in productosByCompras:
            Compras.objects.filter(id_cliente = request.GET['cliente']).filter(
                    precio = None).filter(id_producto = p).update(precio = p.precio)
                    
        total = Compras.objects.filter(id_cliente = request.GET['cliente']).aggregate(Sum('precio'))
        #Log
        Log.objects.create(fecha = datetime.datetime.now(), descripcion="Compra Consultada y Actualizada")
        
    return render(request,'compras/manejar_factura.html', {'formset': formset, 
                                                           'cliente':cliente,
                                                           'total':total['precio__sum']
                                                           })

def pdf_factura(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'atachment; filename=factura-report.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    #Lógica de la factura
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30, 750, 'Factura')
    
    c.setFont('Helvetica', 12)
    c.drawString(30, 735, str(datetime.datetime.now()) )
    
    cliente = Clientes.objects.get(pk=request.GET['cliente'])
    c.drawString(30, 700, "Cliente: " + str( cliente.nombres ))
    c.drawString(30, 685, "Documento: " + str( cliente.documento ))
    
    #Table Header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontsize = 10
    
    productos = Paragraph('''Producto''',styleBH)
    sedes = Paragraph('''Sede''',styleBH)
    precios = Paragraph('''Precio''',styleBH)
    
    data = []
    data.append([productos, sedes, precios])
    
    #Table
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7
    
    high = 640
    
    #Se trae el precio de producto si las compras no lo registran
    comprasByCliente = Compras.objects.filter(id_cliente = request.GET['cliente']).filter(
                    precio = None).order_by('id_producto').values_list('id_producto',flat=True)
    productosByCompras = Productos.objects.filter(id__in = list(comprasByCliente))
        
    for p in productosByCompras:
        Compras.objects.filter(id_cliente = request.GET['cliente']).filter(
                    precio = None).filter(id_producto = p).update(precio = p.precio)
                    
    total = Compras.objects.filter(id_cliente = request.GET['cliente']).aggregate(Sum('precio'))
    
    #Se rellena la tabla 
    
    compras = Compras.objects.filter(id_cliente = request.GET['cliente'])
    
    for compra in compras:
        data.append([compra.id_producto, compra.id_sede, compra.precio])
        high = high -18
    
    width, height = A4
    table = Table(data, colWidths=[3 * cm, 2.5 * cm, 2.5 * cm])
    table.setStyle(TableStyle([
                              ('INNERGRID',(0,0),(-1,-1), 0.25,colors.black),
                              ('BOX',(0,0),(-1,-1), 0.25,colors.black),
                              ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    
    c.setFont('Helvetica', 15)
    c.drawString(30, high - 30, "Total Precio: " + str( total['precio__sum']) )
    
    #Termina lógica de la factura
    c.showPage()
    c.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def pdf_reporte_semanal(request):
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'atachment; filename=factura-report.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    #Lógica de la factura
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30, 750, 'Reporte Semanal')
    
    c.setFont('Helvetica', 12)
    c.drawString(30, 735, str(datetime.datetime.now()) )
    
    #Traer los precios de las compras
    comprasByCliente = Compras.objects.all().exclude(
                    precio = None).order_by('id_producto').values_list('id_producto',flat=True)
    productosByCompras = Productos.objects.filter(id__in = list(comprasByCliente))
    
    promedioCompras = Compras.objects.all().aggregate(Avg('precio'))['precio__avg']
    promedioProducto = productosByCompras.aggregate(Avg('precio'))['precio__avg']
    
    maximaCompras = Compras.objects.all().aggregate(Max('precio'))['precio__max']
    maximaProducto = productosByCompras.aggregate(Max('precio'))['precio__max']
    
    minimaCompras = Compras.objects.all().aggregate(Min('precio'))['precio__min']
    minimaProducto = productosByCompras.aggregate(Min('precio'))['precio__min']
    
    numeroCompras = Compras.objects.all().aggregate(Count('precio'))['precio__count']
    
    totalCompras = Compras.objects.all().aggregate(Sum('precio'))['precio__sum']
    
    c.setFont('Helvetica', 9)
    c.drawString(30, 700, "Promedio Compras: " + str( promedioCompras ))
    c.drawString(300, 700, "Promedio Productos: " + str( promedioProducto ))
    c.drawString(30, 685, "Diferencia Promedio: " + str( promedioProducto -  promedioCompras ))
    
    c.drawString(30, 665, "Máxima Compras: " + str( maximaCompras ))
    c.drawString(300, 665, "Máxima Productos: " + str( maximaProducto ))
    c.drawString(30, 650, "Diferencia Máxima: " + str( maximaProducto -  maximaCompras ))
    
    c.drawString(30, 630, "Mínima Compras: " + str( minimaCompras ))
    c.drawString(300, 630, "Mínima Productos: " + str( minimaProducto ))
    c.drawString(30, 615, "Diferencia Mínima: " + str( minimaProducto -  minimaCompras ))
    
    c.drawString(30, 595, "Número de Compras: " + str( numeroCompras ))
    
    c.drawString(30, 575, "Total Ganancias: " + str( totalCompras ))
    
    c.drawString(30, 555, "Compras Promedio por Minuto: " + str( promedioProducto -  promedioCompras ))
    
    #Termina lógica de la factura
    c.showPage()
    c.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    #response.write(pdf)
    return pdf

def pdf_reporte_semanal_view(request):
    if request.method == "POST":
        EmailMsg = EmailMessage('Prueba','Prueba de contenido',settings.EMAIL_HOST_USER,[request.POST['email']]
                               ,headers={'Reply-To':request.POST['email']})
        pdf = pdf_reporte_semanal(request)
        EmailMsg.attach('reporte_semanal.pdf', pdf, 'application/pdf')
        EmailMsg.send()
        return HttpResponse("El pdf fue enviado al correo sugerido : " + request.POST['email'])
    return render(request, 'compras/index.html')

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
    #Log
    Log.objects.create(fecha = datetime.datetime.now(), descripcion="Producto Consultado")
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
    #Log
    Log.objects.create(fecha = datetime.datetime.now(), descripcion="Sede Consultada")
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
            #Log
            Log.objects.create(fecha = datetime.datetime.now(), descripcion="Compra Agregada")
            return HttpResponseRedirect('/compras/buscarfactura/')
    else:
        data = {'fecha': datetime.datetime.now()}
        form = CompraForm(data)
    return render(request, 'compras/agregar_compra.html', {'form': form})


