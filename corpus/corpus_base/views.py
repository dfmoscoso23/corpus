from django.shortcuts import render, HttpResponse, redirect
from corpus_base.documentador import documentador
from corpus_base.procesos.operaciones import operaciones
from django.contrib import messages
from corpus_base.forms import documentosForm, casosForm, documentosfilterForm, casosconsultaForm, FormularioZonas
from corpus_base.models import casos, temas, zonas, subzonas
from corpus_base.models import documentos as modeldocumentos
from django.contrib.auth.models import User
from corpus_base.procesos import filtros
from corpus_base.procesos.estadisticas import estadisticador
# Create your views here.

def home(request):

	return render(request, "corpus_base/home.html")

def consulta(request):
	form=casosconsultaForm(request.GET)
	opciones_temas= temas.objects.all()
	formulario_zonas=FormularioZonas(request.GET)
	return render(request, "corpus_base/consulta.html",{
		"form":form,
		"opciones_temas":opciones_temas,
		"formulario_zonas":formulario_zonas
		})
def resultado(request):
	form=casosconsultaForm(request.GET)
	opciones_temas= temas.objects.all()
	formulario_zonas=FormularioZonas(request.GET)
	if request.method == 'GET':
		resultado,pre,pos,doc=filtros.filtro_consulta(request)
		resultado_combo=zip(resultado,pre,pos,doc)
		cantidad=estadisticador.conteo_resultados(resultado)
		try:
			est_result=estadisticador(resultado,pre,pos,doc)
			zona_mas, b64, temas_imag=est_result.zoonificacion()
			la_v,la_i,lp_v,lp_i,t_v,t_i,c_v,c_i,lema=est_result.casificador()
			lemas_anteriores=zip(la_v,la_i)
			lemas_posteriores=zip(lp_v,lp_i)
			terminaciones=zip(t_v,t_i)
			clases=zip(c_v,c_i)
			lema =lema
		except:
			return render(request, "corpus_base/consulta.html",{
				"form":form,
				"opciones_temas":opciones_temas,
				"formulario_zonas":formulario_zonas
				})
		return render(request, "corpus_base/resultado.html",{
			"form":form,
			"resultado":resultado_combo,
			"opciones_temas":opciones_temas,
			"formulario_zonas":formulario_zonas,
			"cantidad":cantidad,
			"zona_mas":zona_mas,
			"imag":b64,
			"imag_temas":temas_imag,
			"lemas_anteriores":lemas_anteriores,
			"lemas_posteriores":lemas_posteriores,
			"terminaciones":terminaciones,
			"clases":clases,
			"lema":lema
			})
def estadisticas(request):
	form=casosconsultaForm(request.GET)
	opciones_temas= temas.objects.all()
	formulario_zonas=FormularioZonas(request.GET)
	if request.method == 'GET':
		print(request.GET)
		resultado,pre,pos,doc=filtros.filtro_consulta(request)
		cantidad=estadisticador.conteo_resultados(resultado)
		return render(request, "corpus_base/estadisticas.html",{
			"form":form,
			"opciones_temas":opciones_temas,
			"formulario_zonas":formulario_zonas,
			"cantidad":cantidad
			})
def load_estadistica(request):
	print("HOLA SOY AJAX")
	foo = request.GET.get('resultado')
	bar = request.GET.get('documento')
	print(foo)
	cantidad=estadisticador.conteo_resultados(foo)
	return render(request, 'corpus_base/estadisticas.html', {'cantidad': cantidad})


def load_subzonas(request):
	zona_id = request.GET.get('zona_id')
	zona = zonas.objects.get(id=zona_id)
	subzonas_obj = subzonas.objects.filter(zona=zona)
	return render(request, 'corpus_base/subzonas2.html', {'subzonas_obj': subzonas_obj})



def documentos(request):
	form = documentosForm(request.POST)
	return render(request, "corpus_base/documentos.html", {'form':form})

def procesando(request):

	if request.method == 'POST':
		#mensaje="Procesando %r" %request.GET["docu"]
		form = documentosForm(request.POST)
		print(request.POST)
		titulo=request.POST['titulo']
		fuente=request.POST['fuente']
		documento=request.POST['documento']
		tipo = request.POST['tipo_documento']
		#fecha = request.POST['fecha_publicacion']
		zona = request.POST['zona']
		subzona = request.POST['subzona']
		tema = request.POST['tema']
		documento = request.POST['documento']
		docu=documentador(titulo,tipo,fuente, zona, subzona, tema, documento)
		if form.is_valid():
			form.save(commit=False)
			form.instance.usuario=request.user
			form.save()
			lista = docu.tokenizador()
			return render(request,"corpus_base/procesando.html",{"documento":documento,"lista":lista})
		else:
			messages.success(request, f'El título ya existía'+str(form.errors))
			return render(request, "corpus_base/documentos.html", {'form':form})
	else:
		form = documentosForm(request.POST)
		#messages.success(request, f'No has enviado nada')

def correccion(request):
	if request.method == 'GET':
		documento_filtrado=request.GET.get('documento', 33)
		documento=modeldocumentos.objects.get(id=documento_filtrado)
		documento_text=getattr(documento, 'documento')
		formfiltro=documentosfilterForm(request.GET or None, instance=documento)
		caso=casos.objects.filter(documento = documento)
		#insta= casos.objects.get(id=4)
		#formcas = casosForm(request.POST or None, instance=insta)
		formulario_casos=list()
		ids=list()
		for cas in caso:
			ids.append(cas.id)
			insta=casos.objects.get(id=cas.id)
			formcas = casosForm(request.POST or None, instance=insta)
			formulario_casos.append(formcas)
		lista_general=zip(ids,formulario_casos)
		return render(request, "corpus_base/correccion.html",{"casos":lista_general,"formulario":formfiltro,"documento":documento_text})
	if request.method == 'POST':
		print(request.POST)
		print(type(request.POST.getlist('id')))
		print(request.POST.getlist('id'))
		if len(request.POST.getlist('id'))> 1:
			for item in range(len(request.POST.getlist('id'))):
				print(item)
				data={
				"caso":request.POST.getlist('caso')[item],
				"lema":request.POST.getlist('lema')[item],
				"desinencia":request.POST.getlist('desinencia')[item],
				"prefijos":request.POST.getlist('prefijos')[item],
				"clase_de_palabra":request.POST.getlist('clase_de_palabra')[item],
				"determinante_1":request.POST.getlist('determinante_1')[item],
				"determinante_2":request.POST.getlist('determinante_2')[item],
				"determinante_3":request.POST.getlist('determinante_3')[item]
				}
				cambio=casosForm(data, instance=casos.objects.get(id=request.POST.getlist('id')[item]))
				cambio.save()
			documento_filtrado=request.GET.get('documento', 33)
			doc_modificado=modeldocumentos.objects.get(id=documento_filtrado)
			doc_modificado.revisado=True
			doc_modificado.save()
		else:
			print(request.POST['caso'])
			# cambio=casosForm(request.POST, instance=casos.objects.get(id=request.POST['id']))
			# cambio.save()
		documento_filtrado=request.GET.get('documento', 33)
		return redirect("/corregir/?documento="+documento_filtrado)

