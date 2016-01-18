from .models import Clientes, Productos, Sedes, Compras
from django.forms import modelform_factory, SelectDateWidget, modelformset_factory, inlineformset_factory
import datetime


ClienteForm =  modelform_factory(Clientes, fields=("documento","nombres","detalles"))
ProductoForm = modelform_factory(Productos, fields=("producto","precio","descripcion"))
SedeForm = modelform_factory(Sedes, fields=("sede","direccion"))
CompraForm = modelform_factory(Compras, fields=("id_cliente", "id_producto", "id_sede", "precio",
                                                "descripcion", "fecha"), 
                                widgets = {
                                            'fecha': SelectDateWidget(),
                                        })

CompraFormSet = inlineformset_factory(Clientes, Compras, form= CompraForm, fk_name='id_cliente', extra=0)
