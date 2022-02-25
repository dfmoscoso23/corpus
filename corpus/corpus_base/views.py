from django.shortcuts import render, HttpResponse
from corpus_base.documentador import documentador
from django.contrib import messages
from corpus_base.forms import documentosForm
from corpus_base.models import casos

# Create your views here.

def home(request):

	return render(request, "corpus_base/home.html")

def consulta(request):



	return render(request, "corpus_base/consulta.html")
def documentos(request):
	form = documentosForm(request.POST)

	return render(request, "corpus_base/documentos.html", {'form':form})

def procesando(request):
	if request.method == 'POST':
		#mensaje="Procesando %r" %request.GET["docu"]
		form = documentosForm(request.POST)
		titulo=request.POST['titu']
		fuente=request.POST['fuen']
		documento=request.POST['docu']
		tipo = 0
		fecha = "17/05/2022"
		zona = 0
		subzona = 0
		tema = 0
		docu=documentador(titulo,tipo,fuente, fecha, zona, subzona, tema, documento)
		if docu.is_valid():
			docu.guardarlo()
			lista=docu.tokenizador()
			return render(request,"corpus_base/procesando.html",{"documento":documento,"lista":lista})
		else:
			messages.success(request, f'El título ya existía')
	else:
		form = documentosForm(request.POST)
		#messages.success(request, f'No has enviado nada')

def correccion(request):
	caso=casos.objects
	return render(request, "corpus_base/correccion.html",{"casos":caso})
