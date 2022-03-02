from django.db import models
from corpus_base.procesos.operaciones import operaciones


# Create your models here.

class tipo_documento (models.Model):
	id=models.IntegerField()
	tipo=models.CharField(max_length=35, primary_key=True)
	def __str__ (self):
		return self.tipo

class fuente (models.Model):
	id = models.AutoField(primary_key=True) 
	fuente = models.CharField(max_length=35)
	link = models.CharField(max_length=200)
	referencia = models.CharField(max_length=250)
	def __str__ (self):
		return self.fuente

class zonas (models.Model):
	id=models.IntegerField()
	zona = models.CharField(max_length=35, primary_key=True)
	def __str__ (self):
		return self.zona

class subzonas (models.Model):
	id=models.IntegerField()
	zona = models.ForeignKey(zonas, on_delete=models.CASCADE)
	subzona = models.CharField(max_length=35, primary_key=True)
	def __str__ (self):
		return self.subzona

class temas (models.Model):
	id=models.IntegerField()
	tema = models.CharField(max_length=35, primary_key=True)
	def __str__ (self):
		return self.tema

class documentos (models.Model):
	id=models.AutoField(primary_key=True)
	titulo = models.CharField(max_length=120)
	tipo_documento = models.ForeignKey(tipo_documento, on_delete=models.CASCADE)
	fuente = models.ForeignKey(fuente, on_delete=models.CASCADE)
	fecha_incorporacion = models.DateField(auto_now_add=True, null=True)
	fecha_publicacion  = models.DateField()
	zona = models.ForeignKey(zonas, on_delete=models.CASCADE)
	subzona = models.ForeignKey(subzonas, on_delete=models.CASCADE)
	tema = models.ForeignKey(temas, on_delete=models.CASCADE)
	parrafos = models.IntegerField()
	extension_tokens = models.IntegerField()
	documento = models.CharField(max_length=25000)
	def save(self, *args, **kwargs):
		self.parrafos = self.documento.count("\n")
		self.extension_tokens= operaciones.conteo_tokens(self.documento)
		super().save(*args, **kwargs)
	def __str__ (self):
		return str(self.id) +" " +self.titulo 

class lemas (models.Model):
	id=models.AutoField(primary_key=True)
	lema = models.CharField(max_length=30)
	def __str__ (self):
		return self.lema

class clases_de_palabras (models.Model):
	id=models.IntegerField()
	clase  = models.CharField(max_length=30, primary_key=True)
	determinante_1 = models.CharField(max_length=30,null=True,blank=True)
	determinante_2 = models.CharField(max_length=30,null=True,blank=True)
	determinante_3 = models.CharField(max_length=30,null=True,blank=True)

	def __str__ (self):
		return self.clase# +" "+str(self.determinante_1)+" "+str(self.determinante_2)+" "+str(self.determinante_3)

class determinante_1 (models.Model):
	id = models.AutoField(primary_key=True)
	determinante = models.CharField(max_length=45)
	tipo = models.CharField(max_length=30)
	def __str__ (self):
		return self.tipo +" "+ self.determinante

class determinante_2 (models.Model):
	id = models.AutoField(primary_key=True)
	determinante = models.CharField(max_length=45)
	tipo = models.CharField(max_length=30)
	def __str__ (self):
		return self.tipo +" "+ self.determinante

class determinante_3 (models.Model):
	id = models.AutoField(primary_key=True)
	determinante = models.CharField(max_length=45)
	tipo = models.CharField(max_length=30)
	def __str__ (self):
		return self.tipo +" "+ self.determinante

class casos (models.Model):
	id = models.AutoField(primary_key=True)
	documento = models.ForeignKey(documentos, on_delete=models.CASCADE,blank=True)
	caso = models.CharField(max_length=35,blank=True)
	lema  = models.ForeignKey(lemas, on_delete=models.CASCADE,blank=True)
	mayuscula  = models.BooleanField(default=False,blank=True)
	posicion = models.IntegerField(blank=True)
	lema_anterior = models.CharField(max_length=35,blank=True)#models.ForeignKey(lemas, on_delete=models.CASCADE)
	lema_posterior = models.CharField(max_length=35,blank=True)#models.ForeignKey(lemas, on_delete=models.CASCADE)
	desinencia = models.CharField(max_length=5,blank=True)
	prefijos = models.CharField(max_length=5,blank=True)
	clase_de_palabra = models.ForeignKey(clases_de_palabras, on_delete=models.CASCADE,blank=True)
	determinante_1 = models.ForeignKey(determinante_1, on_delete=models.CASCADE,null=True,blank=True)
	determinante_2 = models.ForeignKey(determinante_2, on_delete=models.CASCADE,null=True,blank=True)
	determinante_3 = models.ForeignKey(determinante_3, on_delete=models.CASCADE,null=True,blank=True)
	def __str__ (self):
		return str(self.id) + " "+ self.caso

