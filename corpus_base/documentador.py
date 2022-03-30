from datetime import date, datetime
import re
from corpus_base.models import documentos, tipo_documento,fuente, zonas, subzonas,temas, clases_de_palabras, determinante_1,determinante_2,determinante_3,determinante_4, casos, lemas
import pickle
import pandas as pd
import spacy
from spacy import displacy
nlp = spacy.load('es_core_news_md')

class documentador():

	def __init__(self,titulo,tipo,fuente, zona, subzona, tema, documento):
		self.titulo= titulo
		self.tipo_documento = tipo
		self.fuente = fuente
		self.fecha_incorporacion = date.today()
		#self.fecha_publicacion  = datetime.strptime(fecha,"%d/%m/%Y")
		self.zona = zona
		self.subzona = subzona
		self.tema = tema
		#self.parrafos = documento.count("\n")
		#self.extension_tokens = len(wordpunct_tokenize(documento))
		self.documento = documento
	def guardarlo(self):
		docu=documentos(
			titulo=self.titulo[:120],
			tipo_documento = tipo_documento.objects.get(id = self.tipo_documento),
			fuente = fuente.objects.get(id = int(self.fuente)),
			fecha_incorporacion = self.fecha_incorporacion,
			#fecha_publicacion = self.fecha_publicacion,
			zona = zonas.objects.get(id = int(self.zona)),
			subzona = subzonas.objects.get(id = int(self.subzona)),
			tema = temas.objects.get(id = int(self.tema)),
			parrafos = self.parrafos,
			extension_tokens = self.extension_tokens,
			documento = self.documento
			)
		docu.save()
	def desinenciador(self,token):
		if bool(re.search(r'[aeiouáéíóú]$',token)):
			if bool(re.search(r'[aeioulrháéíóú]$',token[:-1])):
				if bool(re.search(r'[aeiouáéíóú]$',token[:-1])):
					if bool(re.search(r'[aeiouáéíóú]$',token[:-2])):
						desinencia=token[-4:]
					else:
						desinencia=token[-3:]
				else:
					if bool(re.search(r'[aeiouáéíóú]$',token[:-2])):
						desinencia=token[-2:]
					else:
						desinencia=token[-3:]
			else:
				desinencia=token[-2:]
		else:
			if bool(re.search(r'[aeiouáéíóú]$',token[:-2])):
				desinencia=token[-4:]
			else:
				desinencia=token[-3:]
		return desinencia
	def prefijador(self,token):
		if bool(re.search(r'^[aeiouáéíóú]',token)):
			prefijo=token[:2]
		else:
			if bool(re.search(r'^[aeiouáéíóú]',token[1:])):
				if bool(re.search(r'^[aeiouáéíóú]',token[2:])):
					if bool(re.search(r'^[aeiouáéíóú]',token[4:])):
						prefijo=token[:3]
					else:
						prefijo=token[:4]
				else:
					if bool(re.search(r'^[aeiouáéíóú]',token[3:])):
						prefijo=token[:2]
					else:
						prefijo=token[:3]
			else:
				if bool(re.search(r'^[aeiouáéíóú]',token[2:])):
					if bool(re.search(r'^[aeiouáéíóú]',token[3:])):
						prefijo=token[:4]
					else:
						prefijo=token[:3]
				else:
					print("2")
					prefijo=token[:2]
		return prefijo

	def tokenizador(self):
		documento_limpio=re.sub(r'([\w\.\,\"])\n([\w\.\,\"])',r'\1 \2',self.documento)
		documento_limpio=documento_limpio.replace("\n","")
		documento_limpio=documento_limpio.replace("\r","")
		documento_limpio=documento_limpio.replace("\t","")
		tokens=nlp(documento_limpio)
		lista=[]
		for i,token in enumerate(tokens):
			lema= token.lemma_ #self.lematizador(token.lower())
			self.guardarlema(lema)
			mayuscula=bool(re.search(r'\A[A-Z]',token.text ))
			posicion=i
			if i == 0:
				lema_anterior=""
				lema_posterior = tokens[i+1].lemma_#self.lematizador(tokens[i+1].lower())
			elif i == len(tokens)-1:
				lema_posterior=""
				lema_anterior = tokens[i-1].lemma_#self.lematizador(tokens[i-1].lower())
			else:
				lema_anterior = tokens[i-1].lemma_#self.lematizador(tokens[i-1])
				lema_posterior = tokens[i+1].lemma_#self.lematizador(tokens[i+1])
			desinencia= self.desinenciador(token.text.lower())
			prefijo = self.prefijador(token.text.lower())
			clase, det1, det2, det3, det4 = self.tagger(token)
			clase_de_palabra= clase
			determinante_1 = det1
			determinante_2 = det2
			determinante_3 = det3
			determinante_4 = det4
			caso=(token,lema,mayuscula,posicion,lema_anterior,lema_posterior,desinencia,prefijo,clase_de_palabra,determinante_1,determinante_2,determinante_3,determinante_4)
			lista.append(caso)
			self.guardarcasos(caso)
			print(token,mayuscula,posicion,desinencia,prefijo,lema)
		return lista
	def lemmascrapper(token):
		'''
		Escrapea en the free dictionary la palabra recibida y busca su lema, 
		si no lo encuentra devuelve un error
		'''
		url="https://es.thefreedictionary.com/"+token
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		req = requests.get(url, headers=headers)
		soup= BeautifulSoup(req.text, "lxml")
		resultado=soup.find('div', class_="content-holder")
		# print(resultado.h1.text,"RESULTADO SCRAP")
		#Control de que sea una palabra real
		if soup.find('div', id="Definition") == None:
			raise ValueError("Esta palabra no lleva a ningún lema")
		else:
			tipo=soup.find('i')
			return resultado.h1.text,tipo.text[0]
	def lematizador(self, token):
		with open(f'corpus_base/procesos/datos/rayo_lemmatizador' , 'rb') as f:
			lemma_ray = pickle.load(f)
		
		try:
			# Busca la palabra en la lista de lemmas
			lemma = lemma_ray[lemma_ray['Form']==token].lemma.values[0].lower()
			#print(token,'encontrado en lemma_ray')
		except:
			try:
				# Busca la palabra en internet
				lemma,tipo =self.lemmascrapper(token)
				#print(token,'encontrado en la web')
				# Guarda la palabra encontrada en a_pickelizar
				with open(f"corpus_base/procesos/datos/a_pickelizar.txt","a") as fh:
					try:
						fh.write(str(lemma)+","+str(tipo)+";")
					except UnicodeEncodeError:
						pass
						#print(str(lemma), str(tipo))
			except:
				# Si no la encuentra
				# Guarda la palabra en nombres_propios
				lemma=""
				with open(f"corpus_base/procesos/datos/sinlema.txt","a") as fh:
					try:
						fh.write(str(token)+"\n")
					except UnicodeEncodeError:
						pass
		return lemma
	def guardarlema(self, lema_entry):
		lem=lemas.objects.filter(lema=lema_entry)
		if len(lem)==0:
			glem=lemas(lema=lema_entry)
			glem.save()
			
	def guardarcasos(self, caso):
		if (caso[9] =="") & (caso[10] =="") & (caso[11] =="") & (caso[12] ==""):
			cas=casos(
				documento=documentos.objects.get(titulo=self.titulo),
				caso=caso[0],
				lema=lemas.objects.get(lema=caso[1]),
				mayuscula=caso[2],
				posicion=caso[3],
				lema_anterior=caso[4],
				lema_posterior=caso[5],
				desinencia=caso[6],
				prefijos=caso[7],
				clase_de_palabra=clases_de_palabras.objects.get(clase=caso[8])
				#determinante_1=determinante_1.objects.get(determinante=caso[9]),
				# determinante_2=determinante_2.objects.get(determinante=caso[10]),
				# determinante_3=determinante_3.objects.get(determinante=caso[11]),
				# determinante_4=determinante_4.objects.get(determinante=caso[12])
				)
		elif (caso[10] =="") & (caso[11] =="") & (caso[12] ==""):
			cas=casos(
				documento=documentos.objects.get(titulo=self.titulo),
				caso=caso[0],
				lema=lemas.objects.get(lema=caso[1]),
				mayuscula=caso[2],
				posicion=caso[3],
				lema_anterior=caso[4],
				lema_posterior=caso[5],
				desinencia=caso[6],
				prefijos=caso[7],
				clase_de_palabra=clases_de_palabras.objects.get(clase=caso[8]),
				determinante_1=determinante_1.objects.get(determinante=caso[9]),
				#determinante_2=determinante_2.objects.get(determinante=caso[10]),
				# determinante_3=determinante_3.objects.get(determinante=caso[11]),
				#determinante_4=determinante_4.objects.get(determinante=caso[12])
				)
		elif (caso[9] !="") & (caso[10] !="") &  (caso[11] =="") & (caso[12] ==""):
			print(caso[9])
			cas=casos(
				documento=documentos.objects.get(titulo=self.titulo),
				caso=caso[0],
				lema=lemas.objects.get(lema=caso[1]),
				mayuscula=caso[2],
				posicion=caso[3],
				lema_anterior=caso[4],
				lema_posterior=caso[5],
				desinencia=caso[6],
				prefijos=caso[7],
				clase_de_palabra=clases_de_palabras.objects.get(clase=caso[8]),
				determinante_1=determinante_1.objects.get(determinante=caso[9]),
				determinante_2=determinante_2.objects.get(determinante=caso[10]),
				#determinante_3=determinante_3.objects.get(determinante=caso[11]),
				#determinante_4=determinante_4.objects.get(determinante=caso[12])
				)
		elif (caso[9] !="") & (caso[10] !="") & (caso[12] =="")& (caso[11] !=""):
			cas=casos(
				documento=documentos.objects.get(titulo=self.titulo),
				caso=caso[0],
				lema=lemas.objects.get(lema=caso[1]),
				mayuscula=caso[2],
				posicion=caso[3],
				lema_anterior=caso[4],
				lema_posterior=caso[5],
				desinencia=caso[6],
				prefijos=caso[7],
				clase_de_palabra=clases_de_palabras.objects.get(clase=caso[8]),
				determinante_1=determinante_1.objects.get(determinante=caso[9]),
				determinante_2=determinante_2.objects.get(determinante=caso[10]),
				determinante_3=determinante_3.objects.get(determinante=caso[11]),
				#determinante_4=determinante_4.objects.get(determinante=caso[12])
				)
		elif (caso[10] !="") & (caso[9] =="") & (caso[11] ==""):
			cas=casos(
				documento=documentos.objects.get(titulo=self.titulo),
				caso=caso[0],
				lema=lemas.objects.get(lema=caso[1]),
				mayuscula=caso[2],
				posicion=caso[3],
				lema_anterior=caso[4],
				lema_posterior=caso[5],
				desinencia=caso[6],
				prefijos=caso[7],
				clase_de_palabra=clases_de_palabras.objects.get(clase=caso[8]),
				#determinante_1=determinante_1.objects.get(determinante=caso[9]),
				determinante_2=determinante_2.objects.get(determinante=caso[10]),
				#determinante_3=determinante_3.objects.get(determinante=caso[11])
				#determinante_4=determinante_4.objects.get(determinante=caso[12])
				)
		elif (caso[10] =="") & (caso[9] =="") & (caso[11] !=""):
			cas=casos(
				documento=documentos.objects.get(titulo=self.titulo),
				caso=caso[0],
				lema=lemas.objects.get(lema=caso[1]),
				mayuscula=caso[2],
				posicion=caso[3],
				lema_anterior=caso[4],
				lema_posterior=caso[5],
				desinencia=caso[6],
				prefijos=caso[7],
				clase_de_palabra=clases_de_palabras.objects.get(clase=caso[8]),
				#determinante_1=determinante_1.objects.get(determinante=caso[9]),
				#determinante_2=determinante_2.objects.get(determinante=caso[10]),
				determinante_3=determinante_3.objects.get(determinante=caso[11])
				#determinante_4=determinante_4.objects.get(determinante=caso[12])
				)
		elif (caso[10] =="") & (caso[9] !="") & (caso[11] !=""):
			cas=casos(
				documento=documentos.objects.get(titulo=self.titulo),
				caso=caso[0],
				lema=lemas.objects.get(lema=caso[1]),
				mayuscula=caso[2],
				posicion=caso[3],
				lema_anterior=caso[4],
				lema_posterior=caso[5],
				desinencia=caso[6],
				prefijos=caso[7],
				clase_de_palabra=clases_de_palabras.objects.get(clase=caso[8]),
				determinante_1=determinante_1.objects.get(determinante=caso[9]),
				#determinante_2=determinante_2.objects.get(determinante=caso[10]),
				determinante_3=determinante_3.objects.get(determinante=caso[11])
				#determinante_4=determinante_4.objects.get(determinante=caso[12])
				)
		else:
			cas=casos(
				documento=documentos.objects.get(titulo=self.titulo),
				caso=caso[0],
				lema=lemas.objects.get(lema=caso[1]),
				mayuscula=caso[2],
				posicion=caso[3],
				lema_anterior=caso[4],
				lema_posterior=caso[5],
				desinencia=caso[6],
				prefijos=caso[7],
				clase_de_palabra=clases_de_palabras.objects.get(clase=caso[8]),
				determinante_1=determinante_1.objects.get(determinante=caso[9]),
				determinante_2=determinante_2.objects.get(determinante=caso[10]),
				determinante_3=determinante_3.objects.get(determinante=caso[11]),
				determinante_4=determinante_4.objects.get(determinante=caso[12])
				)			
		cas.save()
	def tagger(self, token):
		dic_numero={"Sing":"Singular","Plur":"Plural"}
		dic_modo={"Imp":"imperativo","Ind":"indicativo","Sub":"subjuntivo"}
		dic_persona={"1":'primera',"2":"segunda","3":"tercera"}
		dic_tiempo={
			"Pres":"presente",
			"Past":"pretérito perfecto simple",
			"Imp":"pretérito imperfecto",
			"Fut":"futuro simple"                    
		}
		dic_genero={"Masc":"Masculino","Fem":"Femenino","Neut":"Neutro"}
		dic_numeral={"Card":"cardinal","Ord":"ordinal","Part":"partitivo"}
		if token.pos_ == "ADJ":
			clase="adjetivo"
			dic=token.morph.to_dict()
			try:
				numero=dic['Number']
				det1=dic_numero[numero]
			except:
				det1=""
			try:
				genero=dic['Gender']
				det2=dic_genero[genero]
			except:
				det2=""
			det3=""
			det4=""
		elif token.pos_ == "ADP":
			clase="preposición"
			det1=""
			det2=""
			det3=""
			det4=""
		elif token.pos_ == "ADV":
			clase="adverbio"
			det1=""
			det2=""
			det3=""
			det4=""
		elif token.pos_ == "AUX":
			clase="verbo"
			dic=token.morph.to_dict()
			try:
				if dic['VerbForm']=="Inf":
					det2="infinitivo simple"
					det1=""
					det3=""
					det4=""
				elif dic['VerbForm']=="Part":
					det2="participio de pasado"
					det1=""
					det3=""
					det4=""
				elif dic['VerbForm']=="Ger":
					det2="gerundio simple"
					det1=""
					det3=""
					det4=""
				else:
					try:
						modo=dic['Mood']
						det1=dic_modo[modo]
					except:
						det1=""
					try:
						tiempo=dic['Tense']
						det2=dic_tiempo[tiempo]
					except:
						det2=""
					try:
						persona=dic['Person']
						det3=dic_persona[persona]
					except:
						det3=""
					try:
						numero=dic['Number']
						det4=dic_numero[numero]
					except:
						det4=""
			except:
				det1=""
				det2=""
				det3=""
				det4=""
		elif token.pos_ == "CCONJ":
			clase="conjunción"
			try:
				det1="coordinante"
			except:
				det1="" 
			det2=""
			det3=""
			det4=""
		elif token.pos_ == "DET":
			dic=token.morph.to_dict()
			try:
				preclase=dic['PronType']
				if preclase=="Art":
					clase="artículo"
					try:
						numero=dic['Number']
						det1=dic_numero[numero]
					except:
						det1=""
					try:
						genero=dic['Gender']
						det2=dic_genero[genero]
					except:
						det2=""
				else:
					clase="demostrativo"
					try:
						numero=dic['Number']
						det1=dic_numero[numero]
					except:
						det1=""
					try:
						genero=dic['Gender']
						det2=dic_genero[genero]
					except:
						det2="" 
				det3=""
				det4=""
			except:
				clase="artículo"
				det1=""
				det2=""
				det3=""
				det4=""
		elif token.pos_ == "INTJ":
			clase="interjección"
			det1=""
			det2=""
			det3=""
			det4=""
		elif token.pos_ == "NOUN":
			clase="sustantivo"
			dic=token.morph.to_dict()
			try:
				numero=dic['Number']
				det1=dic_numero[numero]
			except:
				det1=""
			try:
				genero=dic['Gender']
				det2=dic_genero[genero]
			except:
				det2=""
			det3=""
			det4=""
		elif token.pos_ == "NUM":
			clase="numeral"
			dic=token.morph.to_dict()
			try:
				numero=dic['Number']
				det1=dic_numero[numero]
			except:
				det1=""
			try:
				genero=dic['Gender']
				det2=dic_genero[genero]
			except:
				det2=""
			try:
				numeral=dic['NumType']
				det3=dic_numeral[numeral]
			except:
				det3=""
			det4=""
		elif token.pos_ == "PART":
			clase="afijo"
			det1=""
			det2=""
			det3=""
			det4=""
		elif token.pos_ == "PRON":
			dic=token.morph.to_dict()
			if dic['PronType']=="Prs":
				clase="pronombre"
				try:
					numero=dic['Number']
					det1=dic_numero[numero]
				except:
					det1=""
				try:
					genero=dic['Gender']
					det2=dic_genero[genero]
				except:
					det2=""
				try:
					persona=dic['Person']
					det3=dic_persona[persona]
				except:
					det3=""
				try:
					dic_casos={"Acc":"acusativo","Dat":"dativo"}
					caso=dic['Case']
					det4=dic_casos[caso]
				except:
					det4=""
			elif dic['PronType']=="Int,Rel":
				clase="relativo"
				try:
					numero=dic['Number']
					det1=dic_numero[numero]
				except:
					det1=""
				try:
					genero=dic['Gender']
					det2=dic_genero[genero]
				except:
					det2=""
				det3=""
				det4=""
			elif dic['PronType']=="Rel":
				clase="relativo"
				try:
					numero=dic['Number']
					det1=dic_numero[numero]
				except:
					det1=""
				try:
					genero=dic['Gender']
					det2=dic_genero[genero]
				except:
					det2=""
				det3=""
				det4=""
			elif dic['PronType']=="Int":
				clase="interrogativo"
				try:
					numero=dic['Number']
					det1=dic_numero[numero]
				except:
					det1=""
				try:
					genero=dic['Gender']
					det2=dic_genero[genero]
				except:
					det2=""
			else:
				clase="desconocido"
				det1=""
				det2=""
			det3=""
			det4=""
		elif token.pos_ == "PROPN":
			clase="sustantivo"
			det1=""
			det2=""
			det3=""
			det4=""
		elif token.pos_ == "PUNCT":
			clase="puntuación"
			det1=""
			det2=""
			det3=""
			det4=""        
		elif token.pos_ == "SCONJ":
			clase="conjunción"
			try:
				det1="subordinante"
			except:
				det1="" 
			det2=""
			det3=""
			det4=""      
		elif token.pos_ == "SYM":
			clase="desconocido"
			det1=""
			det2=""
			det3=""
			det4=""  
		elif token.pos_ == "VERB":
			clase="verbo"
			dic=token.morph.to_dict()
			try:
				if dic['VerbForm']=="Inf":
					det2="infinitivo simple"
					det1=""
					det3=""
					det4=""
				elif dic['VerbForm']=="Part":
					det2="participio de pasado"
					det1=""
					det3=""
					det4=""
				elif dic['VerbForm']=="Ger":
					det2="gerundio simple"
					det1=""
					det3=""
					det4=""
				else:
					try:
						modo=dic['Mood']
						det1=dic_modo[modo]
					except:
						det1=""
					try:
						tiempo=dic['Tense']
						det2=dic_tiempo[tiempo]
					except:
						det2=""
					try:
						persona=dic['Person']
						det3=dic_persona[persona]
					except:
						det3=""
					try:
						numero=dic['Number']
						det4=dic_numero[numero]
					except:
						det4=""
			except:
				det1=""
				det2=""
				det3=""
				det4=""
		elif token.pos_ == "X":
			clase="desconocido"
			det1=""
			det2=""
			det3=""
			det4=""
		elif token.pos_ == "SPACE":
			clase="desconocido"
			det1=""
			det2=""
			det3=""
			det4=""
		return(clase,det1,det2,det3,det4)