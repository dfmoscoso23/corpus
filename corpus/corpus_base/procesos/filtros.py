from corpus_base.models import casos, temas, zonas, subzonas
from corpus_base.models import documentos as modeldocumentos
from corpus_base.procesos.operaciones import operaciones
from django.contrib import messages


def filtro_consulta(request):
	caso_filtrado=request.GET.get('caso')
	lema_filtrado=request.GET.get('lema')
	clase_filtrado=request.GET.get('clase_de_palabra')
	det1_filtrado=request.GET.get('determinante_1')
	det2_filtrado=request.GET.get('determinante_2')
	det3_filtrado=request.GET.get('determinante_3')
	tema_filtrado=request.GET.get('tema')
	zona_filtrado=request.GET.get('zonas_form')
	subzona_filtrado=request.GET.get('subzonas_form')
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
		resultado=casos.objects.none()
	if (tema_filtrado != 'todos') & (tema_filtrado is not None):
		docs_filtrados=modeldocumentos.objects.filter(tema=tema_filtrado).values_list('id')
		resultado=resultado.filter(documento__in=docs_filtrados)
	if (str(zona_filtrado) != '10') & (zona_filtrado is not None):
		docs_filtrados=modeldocumentos.objects.filter(zona__id=zona_filtrado).values_list('id')
		resultado=resultado.filter(documento__in=docs_filtrados)
	if (str(subzona_filtrado) != '10') & (subzona_filtrado is not None)& (subzona_filtrado !=""):
		docs_filtrados=modeldocumentos.objects.filter(zona__id=subzona_filtrado).values_list('id')
		resultado=resultado.filter(documento__in=docs_filtrados)
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
		doc.append(resul.documento)
	#resultado_combo=zip(resultado,pre,pos,doc)
	return resultado,pre,pos,doc