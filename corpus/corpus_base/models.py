from django.db import models


# Create your models here.

class tipo_documento (models.Model):
	id=models.IntegerField()
	tipo=models.CharField(max_length=35, primary_key=True)

class fuente (models.Model):
	id = models.AutoField(primary_key=True) 
	fuente = models.CharField(max_length=35)
	link = models.CharField(max_length=200)
	referencia = models.CharField(max_length=250)

class zonas (models.Model):
	id=models.IntegerField()
	zona = models.CharField(max_length=35, primary_key=True)

class subzonas (models.Model):
	id=models.IntegerField()
	zona = models.ForeignKey(zonas, on_delete=models.CASCADE)
	subzona = models.CharField(max_length=35, primary_key=True)

class temas (models.Model):
	id=models.IntegerField()
	tema = models.CharField(max_length=35, primary_key=True)

class documentos (models.Model):
	id=models.AutoField(primary_key=True)
	titulo = models.CharField(max_length=120)
	tipo_documento = models.ForeignKey(tipo_documento, on_delete=models.CASCADE)
	fuente = models.ForeignKey(fuente, on_delete=models.CASCADE)
	fecha_incorporacion = models.DateField()
	fecha_publicacion  = models.DateField()
	zona = models.ForeignKey(zonas, on_delete=models.CASCADE)
	subzona = models.ForeignKey(subzonas, on_delete=models.CASCADE)
	tema = models.ForeignKey(temas, on_delete=models.CASCADE)
	parrafos = models.IntegerField()
	extension_tokens = models.IntegerField()
	documento = models.CharField(max_length=25000)
	def __str__ (self):
		return self.titulo 

class lemas (models.Model):
	id=models.AutoField(primary_key=True)
	lema = models.CharField(max_length=30)

class clases_de_palabras (models.Model):
	id=models.IntegerField()
	clase  = models.CharField(max_length=30, primary_key=True)
	determinante_1 = models.CharField(max_length=30,null=True,blank=True)
	determinante_2 = models.CharField(max_length=30,null=True,blank=True)
	determinante_3 = models.CharField(max_length=30,null=True,blank=True)

	def __str__ (self):
		return self.clase +" "+str(self.determinante_1)+" "+str(self.determinante_2)+" "+str(self.determinante_3)

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
	documento = models.ForeignKey(documentos, on_delete=models.CASCADE)
	caso = models.CharField(max_length=35)
	lema  = models.ForeignKey(lemas, on_delete=models.CASCADE)
	mayuscula  = models.BooleanField(default=False)
	posicion = models.IntegerField()
	lema_anterior = models.CharField(max_length=35)#models.ForeignKey(lemas, on_delete=models.CASCADE)
	lema_posterior = models.CharField(max_length=35)#models.ForeignKey(lemas, on_delete=models.CASCADE)
	desinencia = models.CharField(max_length=5)
	prefijos = models.CharField(max_length=5)
	clase_de_palabra = models.ForeignKey(clases_de_palabras, on_delete=models.CASCADE)
	determinante_1 = models.ForeignKey(determinante_1, on_delete=models.CASCADE,null=True,blank=True)
	determinante_2 = models.ForeignKey(determinante_2, on_delete=models.CASCADE,null=True,blank=True)
	determinante_3 = models.ForeignKey(determinante_3, on_delete=models.CASCADE,null=True,blank=True)

