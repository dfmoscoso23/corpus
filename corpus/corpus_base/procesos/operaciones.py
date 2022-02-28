import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize

class operaciones():
	def conteo_tokens(documento):
		return len(wordpunct_tokenize(documento))
	def tokenizador(documento):
		return wordpunct_tokenize(documento)