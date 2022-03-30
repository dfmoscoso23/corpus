from django.shortcuts import render
from acercade.estadiador import estadiador
from autenticacion.models import Profile
from django.contrib.auth.models import User


# Create your views here.

def acercade(request):
	return render(request, "acercade/acercade.html")
def colaboradores(request):
	datos_perfiles=Profile.objects.all()
	usuarios=list()
	for dato in datos_perfiles:
		usuarios.append(User.objects.get(id=dato.user_id))
	pefiles= zip(usuarios,datos_perfiles)
	return render(request, "acercade/colaboradores.html",{"perfiles":pefiles})
def estado(request):
	cant_total, img_zonas, img_tipo, img_tema =estadiador.estadodocumentos()
	cant_formas,casos_unicos,cant_lemas=estadiador.estadocasos()

	return render(request, "acercade/estado.html",{
		"cant_total":cant_total,
		"cant_formas":cant_formas,
		"casos_unicos":casos_unicos,
		"cant_lemas":cant_lemas,
		"img_zonas":img_zonas,
		"img_tipo":img_tipo,
		"img_tema":img_tema
		})