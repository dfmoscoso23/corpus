from django.contrib import admin
from corpus_base.models import tipo_documento, fuente, zonas, subzonas, temas, documentos, lemas, clases_de_palabras, determinante_1, determinante_2, determinante_3, determinante_4, casos

# Register your models here.

admin.site.register(tipo_documento)
admin.site.register(fuente)
admin.site.register(zonas)
admin.site.register(subzonas)
admin.site.register(temas)
admin.site.register(documentos)
admin.site.register(lemas)
admin.site.register(clases_de_palabras)
admin.site.register(determinante_1)
admin.site.register(determinante_2)
admin.site.register(determinante_3)
admin.site.register(determinante_4)
admin.site.register(casos)