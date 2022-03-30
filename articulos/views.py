from django.shortcuts import render
from articulos.models import articulos as modelarticulos
from django.contrib import messages

# Create your views here.
def articulos(request):
	articulos = modelarticulos.objects.all()
	if len(articulos) == 0:
		messages.success(request, f'Todavía no se han publicado artículos.')
		return render(request, "articulos/articulos.html")
	return render(request, "articulos/articulos.html",{'articulos':articulos})

def articulo_desplegado(request):
	art_id = request.GET.get('art')
	print(art_id)
	try:
		articulo = modelarticulos.objects.get(id=art_id)
	except:
		messages.success(request, f'No existe el documento')
		return render(request, "articulos/articulos.html")
	return render(request, "articulos/articulo_despliegue.html", {'articulo':articulo})