from django.shortcuts import render, HttpResponse, redirect
from corpus_base.documentador import documentador
from corpus_base.procesos.operaciones import operaciones
from django.contrib import messages
from corpus_base.forms import documentosForm, casosForm, documentosfilterForm, casosconsultaForm
from corpus_base.models import casos
from corpus_base.models import documentos as modeldocumentos
# Create your views here.

def home(request):

	return render(request, "corpus_base/home.html")

def consulta(request):
	form=casosconsultaForm(request.GET)
	if request.method == 'GET':
		caso_filtrado=request.GET.get('caso')
		lema_filtrado=request.GET.get('lema')
		clase_filtrado=request.GET.get('clase_de_palabra')
		det1_filtrado=request.GET.get('determinante_1')
		det2_filtrado=request.GET.get('determinante_2')
		det3_filtrado=request.GET.get('determinante_3')
		if caso_filtrado!='' and caso_filtrado is not None:
			resultado=casos.objects.filter(
				caso=caso_filtrado
				)
		elif lema_filtrado!='' and lema_filtrado is not None:
			resultado=casos.objects.filter(
				lema=lema_filtrado
				)
		elif clase_filtrado!='' and clase_filtrado is not None:
			resultado=casos.objects.filter(
				clase_de_palabra=clase_filtrado
				)
		elif det1_filtrado!='' and det1_filtrado is not None:
			resultado=casos.objects.filter(
				determinante_1=det1_filtrado
				)
		elif det2_filtrado!='' and det2_filtrado is not None:
			resultado=casos.objects.filter(
				determinante_2=det2_filtrado
				)
		elif det3_filtrado!='' and det3_filtrado is not None:
			resultado=casos.objects.filter(
				determinante_3=det3_filtrado
				)
		else:
			messages.success(request, f'No se encontró una búsqueda')
			resultado=""
		documentos=list()
		pre=list()
		pos=list()
		doc=list()
		for resul in resultado:
			print(resul.posicion)
			tokens=operaciones.tokenizador(resul.documento.documento)
			if resul.posicion > 12:
				pre_contexto = "..."
				for i in range((resul.posicion-12),resul.posicion):
					if tokens[i] in [".",",","!","?","¡","¿","'",":",";"]:
						pre_contexto+=tokens[i]
					else:
						pre_contexto+=" "+tokens[i]
				pre.append(pre_contexto)
			elif resul.posicion != 0:
				pre_contexto = str()
				for i in range(0,resul.posicion):
					if tokens[i] in [".",",","!","?","¡","¿","'",":",";"]:
						pre_contexto+=tokens[i]
					else:
						pre_contexto+=" "+tokens[i]
				pre.append(pre_contexto)	
			else:
				pre_contexto = ""
				pre.append(pre_contexto)
			if len(tokens) > (resul.posicion+12):
				pos_contexto = str()
				for i in range((resul.posicion+1),(resul.posicion+12)):
					if tokens[i] in [".",",","!","?","¡","¿","'",":",";"]:
						pos_contexto+=tokens[i]
					else:
						pos_contexto+=" "+tokens[i]
				pos_contexto+="..."
				pos.append(pos_contexto)
			elif len(tokens) != resul.posicion:
				pos_contexto = str()
				for i in range((resul.posicion+1),(len(tokens))):
					if tokens[i] in [".",",","!","?","¡","¿","'",":",";"]:
						pos_contexto+=tokens[i]
					else:
						pos_contexto+=" "+tokens[i]
				#pos_contexto+="..."
				pos.append(pos_contexto)
			else:
				pos_contexto = str()
				pos.append(pos_contexto)
			doc.append(resul.documento.id)
		resultado_combo=zip(resultado,pre,pos,doc)

		#documentos.append()
		return render(request, "corpus_base/consulta.html",{"form":form,"resultado":resultado_combo})
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
		else:
			print(request.POST['caso'])
			# cambio=casosForm(request.POST, instance=casos.objects.get(id=request.POST['id']))
			# cambio.save()
		documento_filtrado=request.GET.get('documento', 33)
		return redirect("/corregir/?documento="+documento_filtrado)

