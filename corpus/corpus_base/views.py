from django.shortcuts import render, HttpResponse

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

		return render(request,"corpus_base/procesando.html",{"documento":documento})
	else:
		mensaje="No has enviado nada"
	return HttpResponse(mensaje)

def contacto(request):

	return render(request, "corpus_base/contacto.html")