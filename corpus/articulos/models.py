from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class articulos(models.Model):
	titulo = models.CharField(max_length=120,blank=True)
	autor = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
	fecha = models.DateField(auto_now_add=True, null=True)
	documento = models.CharField(max_length=3500,blank=True)
	bibliografia = models.CharField(max_length=500,blank=True)
	publicado = models.BooleanField(default=False,blank=True)
	referencia = models.CharField(max_length=200,blank=True)
	abstract = models.CharField(max_length=300,blank=True)

	def __str__ (self):
		return str(self.autor) +" - " +self.titulo
