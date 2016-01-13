from .models import Clientes, Productos, Sedes
from django.forms import modelform_factory


ClienteForm =  modelform_factory(Clientes, fields=("documento","nombres","detalles"))
ProductoForm = modelform_factory(Productos, fields=("producto","precio","descripcion"))
SedeForm = modelform_factory(Sedes, fields=("sede","direccion"))