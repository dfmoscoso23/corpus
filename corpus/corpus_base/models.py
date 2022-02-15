from django.db import models

# Create your models here.

class tipo_documento (models.Model):
	id=model.IntegerField()
	tipo=model.CharField(max_length=35, primary_key=True)

class fuente (models.Model):
	id=model.IntegerField(primary_key=True) 
	fuente = model.CharField(max_length=35)
	link = model.CharField(max_length=200)
	referencia = model.CharField(max_length=250)

class zonas (models.Model):
	id=model.IntegerField()
	zona = model.CharField(max_length=35, primary_key=True)

class subzonas (models.Model):
	id=model.IntegerField()
	zona = model.ForeignKey(zonas, on_delete=models.CASCADE)
	subzona = model.CharField(max_length=35, primary_key=True)

class temas (models.Model):
	id=model.IntegerField()
	tema = model.CharField(max_length=35, primary_key=True)

class documentos (models.Model):
	id=model.IntegerField(primary_key=True)
	titulo = model.CharField(max_length=35)
	tipo_documento = model.ForeignKey(tipo_documento, on_delete=models.CASCADE)
	fuente = model.ForeignKey(fuente, on_delete=models.CASCADE)
	fecha_incorporacion = model.DateField()
	fecha_publicacion  = model.DateField()
	zona = model.ForeignKey(zonas, on_delete=models.CASCADE)
	subzona = model.ForeignKey(subzonas, on_delete=models.CASCADE)
	zona = model.ForeignKey(temas, on_delete=models.CASCADE)
	parrafos = model.IntegerField()
	extension_tokens = model.IntegerField()
	documento = model.CharField(max_length=25000)

class lemas (models.Model):
	id=model.IntegerField()
	lema  = model.CharField(max_length=30, primary_key=True)

class clases_de_palabras (models.Model):
	id=model.IntegerField()
	clase  = model.CharField(max_length=30, primary_key=True)
	determinante_1 = model.CharField(max_length=30)
	determinante_2 = model.CharField(max_length=30)
	determinante_3 = model.CharField(max_length=30)

class determinante_1 (models.Model):
	id = model.IntegerField()
	determinante = model.CharField(max_length=45)
	tipo = model.CharField(max_length=30)

class determinante_2 (models.Model):
	id = model.IntegerField()
	determinante = model.CharField(max_length=45)
	tipo = model.CharField(max_length=30)

class determinante_3 (models.Model):
	id = model.IntegerField()
	determinante = model.CharField(max_length=45)
	tipo = model.CharField(max_length=30)

class casos (models.Model):
	id = model.IntegerField(primary_key=True)
	documento = model.ForeignKey(documentos, on_delete=models.CASCADE)
	caso = model.CharField(max_length=35)
	lema  = model.ForeignKey(lemas, on_delete=models.CASCADE)
	mayuscula  = models.BooleanField(default=False)
	posicion = model.IntegerField()
	lema_anterior = model.ForeignKey(lemas, on_delete=models.CASCADE)
	lema_posterior = model.ForeignKey(lemas, on_delete=models.CASCADE)
	desinencia = model.CharField(max_length=5)
	prefijos = model.CharField(max_length=5)
	clase_de_palabra = model.ForeignKey(clases_de_palabras, on_delete=models.CASCADE)
	determinante_1 = model.ForeignKey(determinante_1, on_delete=models.CASCADE)
	determinante_2 = model.ForeignKey(determinante_2, on_delete=models.CASCADE)
	determinante_3 = model.ForeignKey(determinante_3, on_delete=models.CASCADE)

