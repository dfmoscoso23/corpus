# import nltk
# from nltk.tokenize import word_tokenize, wordpunct_tokenize
import spacy
from spacy import displacy
nlp = spacy.load('es_core_news_md')
class operaciones():
	def conteo_tokens(documento):
		doc_nlp=nlp(documento)
		return doc_nlp.__len__()
		#return len(wordpunct_tokenize(documento))
	def tokenizador(documento):
		return nlp(documento)
		#return wordpunct_tokenize(documento)