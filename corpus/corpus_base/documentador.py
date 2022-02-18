import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from datetime import date, datetime
from corpus_base.models import documentos, tipo_documento,fuente, zonas, subzonas,temas


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
	def tokenizador(self):
		tokens=wordpunct_tokenize(self.documento)
		for token in tokens:
			pass

