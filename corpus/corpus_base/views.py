from django.shortcuts import render, HttpResponse
from corpus_base.documentador import documentador

# Create your views here.

def home(request):

	return render(request, "corpus_base/home.html")

def documentos(request):



	return render(request, "corpus_base/documentos.html")

def procesando(request):
	if request.method == 'POST':
		#mensaje="Procesando %r" %request.GET["docu"]
		titulo=request.POST['titu']
		fuente=request.POST['fuen']
		documento=request.POST['docu']
		tipo = 0
		fecha = "17/05/2022"
		zona = 0
		subzona = 0
		tema = 0
		docu=documentador(titulo,tipo,fuente, fecha, zona, subzona, tema, documento)
		docu.guardarlo()
		return render(request,"corpus_base/procesando.html",{"documento":documento})
	else:
		mensaje="No has enviado nada"
	return HttpResponse(mensaje)

def contacto(request):

	return render(request, "corpus_base/contacto.html")