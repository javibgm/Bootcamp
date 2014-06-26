# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'license', 'visibility', 'owner_name')  # Añadir columnas a la tabla de objetos
    list_filter = ('license', 'visibility')  # Añadir filtros a la tabla de objetos
    search_fields = ('name', 'description')  ## Añadir campo de busqueda en los campos especificados en la tabla de objetos

    def owner_name(self, obj):
        """
        Indica como tiene que sacar el nombre en la tabla
        :param obj: objeto a representar (en este caso una foto)
        :return: nombre + apellido
        """
        return obj.owner.first_name + " " + obj.owner.last_name

    owner_name.short_description = 'Propietario'  # Nombre de la columna de la tabla
    owner_name.admin_order_field = 'owner'  # Campo por el que ordenar

    # tunnin del detalle (lo que ves al pinchar en un objeto)
    fieldsets = ( # Bloques de campos ( titulo, {'fields': (nombre_campos)} )
        (
            None,  # Bloque sin nombre
            {
                'fields': ('name',)  # En este bloque solo aparecera el nombre
            }
        ),
        (
            'Descripcion y autor',  # Nombre del bloque
            {
                'fields': ('description', 'owner')  # Campos del bloque
            }
        ),
        (
            'URL, licencia y visibilidad',  # Nombre del bloque
            {
                'classes': ('collapse',),  # Para poder ocultar el bloque
                'fields': ('url', 'license', 'visibility')
            }
        )
    )

# Register your models here.

admin.site.register(Photo, PhotoAdmin)  # así relacionamos el objeto con la clase que lo tiene que administrar