from django.shortcuts import render, HttpResponse, redirect
from corpus_base.documentador import documentador
from corpus_base.procesos.operaciones import operaciones
from django.contrib import messages
from corpus_base.forms import documentosForm, casosForm, documentosfilterForm, FormularioZonas
from corpus_base.models import casos, temas, zonas, subzonas, clases_de_palabras, determinante_1, determinante_2, determinante_3, determinante_4, lemas
from corpus_base.models import documentos as modeldocumentos
from django.contrib.auth.models import User
from corpus_base.procesos import filtros
from corpus_base.procesos.estadisticas import estadisticador
from django.core.paginator import Paginator
# Create your views here.

def home(request):

	return render(request, "corpus_base/home.html")

def consulta(request):
	opciones_temas= temas.objects.all()
	formulario_zonas=FormularioZonas(request.GET)
	#formas_consulta=formasConsultaForm(request.GET)
	clases_or=clases_de_palabras.objects.all()
	return render(request, "corpus_base/consulta.html",{
		"opciones_temas":opciones_temas,
		"formulario_zonas":formulario_zonas,
		# "formas_consulta":formas_consulta,
		"clases_or":clases_or
		})
def resultado(request):
	clases_or=clases_de_palabras.objects.all()
	opciones_temas= temas.objects.all()
	formulario_zonas=FormularioZonas(request.GET)
	if request.method == 'GET':
		resultado,pre,pos,doc =filtros.filtro_consulta(request)
		print(len(resultado),"LARGO DEL RESULTADO")
		if len(resultado)==0:
			messages.success(request,f'No se encontró resultados')
			return render(request, "corpus_base/consulta.html",{
				"clases_or":clases_or,
				"opciones_temas":opciones_temas,
				"formulario_zonas":formulario_zonas
				})
		# resultado_combo=zip(resultado,pre,pos,doc)
		cantidad=estadisticador.conteo_resultados(resultado)
		# try:
		est_result=estadisticador(resultado,pre,pos,doc)
		zona_mas, b64, temas_imag=est_result.zoonificacion()
		la_v,la_i,lp_v,lp_i,t_v,t_i,c_v,c_i,lema=est_result.casificador()
		lemas_anteriores=zip(la_v,la_i)
		lemas_posteriores=zip(lp_v,lp_i)
		terminaciones=zip(t_v,t_i)
		clases=zip(c_v,c_i)
		print("CLASES",clases)
		lemas_lista=[]
		print(lema)
		for lem in lema:
			le =lemas.objects.get(id=lem)
			lemas_lista.append(le.lema)
		lema=lemas_lista
		# except:
		# 	return render(request, "corpus_base/consulta.html",{
		# 		"form":form,
		# 		"opciones_temas":opciones_temas,
		# 		"formulario_zonas":formulario_zonas
		# 		})
		pag_result_w=Paginator(resultado,10)
		pag_pre_w=Paginator(pre,10)
		pag_pos_w=Paginator(pos,10)
		pag_doc_w=Paginator(doc,10)
		page_number = request.GET.get('page')
		pag_result = pag_result_w.get_page(page_number)
		pag_pre=pag_pre_w.get_page(page_number)
		pag_pos=pag_pos_w.get_page(page_number)
		pag_doc=pag_doc_w.get_page(page_number)
		resultado_combo=zip(pag_result,pag_pre,pag_pos,pag_doc)
		return render(request, "corpus_base/resultado.html",{
			"clases_or":clases_or,
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
			"lema":lema,
			"pag_result":pag_result
			})

def load_determinantes(request):
	clase_id = request.GET.get('clase_id')
	if clase_id == 'todos':
		tipo = None
		tipo2 = None
		tipo3 = None
		tipo4 = None
		det_1 = None
		det_2 = None
		det_3 = None
		det_4 = None
	else:
		clase = clases_de_palabras.objects.get(clase=clase_id)
		det_1 = determinante_1.objects.filter(tipo=clase.determinante_1)
		tipo = clase.determinante_1
		det_2 = determinante_2.objects.filter(tipo=clase.determinante_2)
		tipo2 = clase.determinante_2
		det_3 = determinante_3.objects.filter(tipo=clase.determinante_3)
		tipo3 = clase.determinante_3
		det_4 = determinante_4.objects.filter(tipo=clase.determinante_4)
		tipo4 = clase.determinante_4
	return render(request, 'corpus_base/deter_1.html', {
		'det_1': det_1,
		'tipo':tipo,
		'det_2':det_2,
		'tipo2':tipo2,
		'det_3':det_3,
		'tipo3':tipo3,
		'det_4':det_4,
		'tipo4':tipo4
		})


def load_subzonas(request):
	zona_id = request.GET.get('zona_id')
	if zona_id == '10':
		tod=None
		subzonas_obj = None
	else:
		tod="fo"
		zona = zonas.objects.get(id=zona_id)
		subzonas_obj = subzonas.objects.filter(zona=zona)
	return render(request, 'corpus_base/subzonas2.html', {'subzonas_obj': subzonas_obj,'tod':tod})



def documentos(request):
	form = documentosForm(request.POST)
	return render(request, "corpus_base/documentos.html", {'form':form})

def procesando(request):

	if request.method == 'POST':
		#mensaje="Procesando %r" %request.GET["docu"]
		form = documentosForm(request.POST)
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
		ultimo_doc=modeldocumentos.objects.first()
		documento_filtrado=request.GET.get('documento', ultimo_doc.id)
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
		if len(request.POST.getlist('id'))> 1:
			for item in range(len(request.POST.getlist('id'))):
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
			documento_filtrado=request.GET.get('documento', int(ultimo_doc.id))
			doc_modificado=modeldocumentos.objects.get(id=documento_filtrado)
			doc_modificado.revisado=True
			doc_modificado.save()
		else:
			print(request.POST['caso'])
			# cambio=casosForm(request.POST, instance=casos.objects.get(id=request.POST['id']))
			# cambio.save()
		documento_filtrado=request.GET.get('documento', int(ultimo_doc.id))
		return redirect("/corregir/?documento="+str(documento_filtrado))

def documento_ficha(request):
	doc_id=request.GET.get('id')
	try:
		documento=modeldocumentos.objects.get(id=doc_id)
	except:
		messages.success(request, f'No existe el documento')
		return render(request, "corpus_base/home.html")
	return render(request, "corpus_base/doc_blog.html", {'documento':documento})


