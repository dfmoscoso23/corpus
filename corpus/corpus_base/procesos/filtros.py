from corpus_base.models import casos, temas, zonas, subzonas, lemas
from corpus_base.models import documentos as modeldocumentos
from corpus_base.procesos.operaciones import operaciones
from django.contrib import messages

def filtro_consulta(request):
	caso_filtrado=request.GET.get('forma_exacta')
	forma_relativa=request.GET.get('forma_relativa')
	lema_filtrado=request.GET.get('lema')
	terminacion=request.GET.get('terminacion')
	clase_filtrado=request.GET.get('clase_de_palabra_form')
	det1_filtrado=request.GET.get('determinante_1_form')
	det2_filtrado=request.GET.get('determinante_2_form')
	det3_filtrado=request.GET.get('determinante_3_form')
	det4_filtrado=request.GET.get('determinante_4_form')
	tema_filtrado=request.GET.get('tema')
	zona_filtrado=request.GET.get('zonas_form')
	subzona_filtrado=request.GET.get('subzonas_form')
	tipo_filtrado=request.GET.get('tipo_documento')
	revisado_filtrado=request.GET.get('revisado')
	if caso_filtrado !='' and caso_filtrado is not None:
		print("FILTRADOOOO",caso_filtrado)
		resultado=casos.objects.filter(
			caso=caso_filtrado
			)
		print(resultado)
	elif forma_relativa !='' and forma_relativa is not None:
		resultado=casos.objects.filter(
			caso__istartswith=forma_relativa
			)
	elif lema_filtrado!='' and lema_filtrado is not None:
		lema_id=lemas.objects.get(lema=lema_filtrado)
		resultado=casos.objects.filter(
			lema=lema_id
			)
	elif terminacion!='' and terminacion is not None:
		resultado=casos.objects.filter(
			desinencia=terminacion
			)
	else:
		messages.success(request, f'No se encontró una búsqueda. Es necesario introducir una forma, un lema o una terminación')
		resultado=casos.objects.none()
	if clase_filtrado!='todos' and clase_filtrado is not None:
		resultado=resultado.filter(
			clase_de_palabra=clase_filtrado
			)
	if det1_filtrado!='' and det1_filtrado is not None:
		resultado=resultado.filter(
			determinante_1=det1_filtrado
			)
	if det2_filtrado!='' and det2_filtrado is not None:
		resultado=resultado.filter(
			determinante_2=det2_filtrado
			)
	if det3_filtrado!='' and det3_filtrado is not None:
		resultado=resultado.filter(
			determinante_3=det3_filtrado
			)
	if (tema_filtrado != 'todos') & (tema_filtrado is not None):
		docs_filtrados=modeldocumentos.objects.filter(tema=tema_filtrado).values_list('id')
		resultado=resultado.filter(documento__in=docs_filtrados)
	if (str(zona_filtrado) != '10') & (zona_filtrado is not None):
		docs_filtrados=modeldocumentos.objects.filter(zona__id=zona_filtrado).values_list('id')
		resultado=resultado.filter(documento__in=docs_filtrados)
	if (str(subzona_filtrado) != '10') & (subzona_filtrado is not None)& (subzona_filtrado !=""):
		docs_filtrados=modeldocumentos.objects.filter(subzona__id=subzona_filtrado).values_list('id')
		resultado=resultado.filter(documento__in=docs_filtrados)
	if (tipo_filtrado != '') & (tipo_filtrado is not None):
		docs_filtrados=modeldocumentos.objects.filter(tipo_documento=tipo_filtrado).values_list('id')
		resultado=resultado.filter(documento__in=docs_filtrados)
	if (revisado_filtrado != '') & (revisado_filtrado is not None):
		if revisado_filtrado == "on":
			revisado_filtrado=True
		else:
			revisado_filtrado=False
		docs_filtrados=modeldocumentos.objects.filter(revisado=revisado_filtrado).values_list('id')
		resultado=resultado.filter(documento__in=docs_filtrados)
	documentos=list()
	pre=list()
	pos=list()
	doc=list()
	for resul in resultado:
		#print("POSICION RESULTADO:",resul.posicion)
		tokens=operaciones.tokenizador(resul.documento.documento)
		if resul.posicion > 12:
			pre_contexto = "..."
			for i in range((resul.posicion-12),resul.posicion):
				#print("TOKEN",i,tokens[i].text)
				if tokens[i].text in [".",",","!","?","¡","¿","'",":",";"]:
					#print("TOKEN",i,tokens[i].text)
					pre_contexto+=tokens[i].text
				else:
					#print("TOKEN",i,tokens[i].text)
					pre_contexto+=" "+tokens[i].text
			pre.append(pre_contexto)
		elif resul.posicion != 0:
			pre_contexto = str()
			for i in range(0,resul.posicion):
				if tokens[i].text in [".",",","!","?","¡","¿","'",":",";"]:
					pre_contexto+=tokens[i].text
				else:
					pre_contexto+=" "+tokens[i].text
			pre.append(pre_contexto)	
		else:
			pre_contexto = ""
			pre.append(pre_contexto)
		if len(tokens) > (resul.posicion+12):
			pos_contexto = str()
			for i in range((resul.posicion+1),(resul.posicion+12)):
				if tokens[i].text in [".",",","!","?","¡","¿","'",":",";"]:
					pos_contexto+=tokens[i].text
				else:
					pos_contexto+=" "+tokens[i].text
			pos_contexto+="..."
			pos.append(pos_contexto)
		elif len(tokens) != resul.posicion:
			pos_contexto = str()
			for i in range((resul.posicion+1),(len(tokens))):
				if tokens[i].text in [".",",","!","?","¡","¿","'",":",";"]:
					pos_contexto+=tokens[i].text
				else:
					pos_contexto+=" "+tokens[i].text
			#pos_contexto+="..."
			pos.append(pos_contexto)
		else:
			pos_contexto = str()
			pos.append(pos_contexto)
		doc.append(resul.documento)
	#resultado_combo=zip(resultado,pre,pos,doc)
	return resultado,pre,pos,doc