from django.contrib import admin

from .models import Clientes, Productos, Sedes, Compras

# Register your models here.

admin.site.register(Clientes)
admin.site.register(Productos)
admin.site.register(Sedes)
admin.site.register(Compras)
