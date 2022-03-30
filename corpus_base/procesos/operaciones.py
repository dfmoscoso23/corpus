# import nltk
# from nltk.tokenize import word_tokenize, wordpunct_tokenize
import spacy
from spacy import displacy
import re
nlp = spacy.load('es_core_news_md')
class operaciones():
	def conteo_tokens(documento):
		doc_nlp=nlp(documento)
		return doc_nlp.__len__()
		#return len(wordpunct_tokenize(documento))
	def tokenizador(documento):
		documento_limpio=re.sub(r'([\w\.\,\"])\n([\w\.\,\"])',r'\1 \2',documento)
		documento_limpio=documento_limpio.replace("\n","")
		documento_limpio=documento_limpio.replace("\r","")
		documento_limpio=documento_limpio.replace("\t","")
		return nlp(documento_limpio)
		#return wordpunct_tokenize(documento)