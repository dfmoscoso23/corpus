import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from datetime import date, datetime
import re
from corpus_base.models import documentos, tipo_documento,fuente, zonas, subzonas,temas
import pickle
import pandas as pd


class documentador():

	def __init__(self,titulo,tipo,fuente, fecha, zona, subzona, tema, documento):
		self.titulo= titulo
		self.tipo_documento = tipo
		self.fuente = fuente
		self.fecha_incorporacion = date.today()
		self.fecha_publicacion  = datetime.strptime(fecha,"%d/%m/%Y")
		self.zona = zona
		self.subzona = subzona
		self.tema = tema
		self.parrafos = documento.count("\n")
		self.extension_tokens = len(wordpunct_tokenize(documento))
		self.documento = documento

	def guardarlo(self):
		docu=documentos(
			titulo=self.titulo[:35],
			tipo_documento = tipo_documento.objects.get(id = self.tipo_documento),
			fuente = fuente.objects.get(id = int(self.fuente)),
			fecha_incorporacion = self.fecha_incorporacion,
			fecha_publicacion = self.fecha_publicacion,
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
		tokens=wordpunct_tokenize(self.documento)
		lista=[]
		for i,token in enumerate(tokens):
			token
			lema= self.lematizador(token.lower())
			mayuscula=bool(re.search(r'\A[A-Z]',token ))
			posicion=i
			if i == 0:
				lema_anterior=""
				lema_posterior = self.lematizador(tokens[i+1].lower())
			elif i == len(tokens)-1:
				lema_posterior=""
				lema_anterior = self.lematizador(tokens[i-1].lower())
			else:
				lema_anterior = self.lematizador(tokens[i-1])
				lema_posterior = self.lematizador(tokens[i+1])
			desinencia= self.desinenciador(token.lower())
			prefijo = self.prefijador(token.lower())
			clase_de_palabra=""
			determinante_1 = ""
			determinante_2 = ""
			determinante_3 = ""
			lista.append((token,mayuscula,posicion,desinencia,prefijo,lema,lema_posterior,lema_anterior))
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
