import pandas as pd
import io, base64
import matplotlib.pyplot as plt



class estadisticador():
	def __init__(self, resultado,pre,pos,doc):
		dic_caso={}
		dic_caso['id']=list()
		dic_caso['caso']=list()
		dic_caso['lema_anterior']=list()
		dic_caso['lema_posterior']=list()
		dic_caso['desinencia']=list()
		dic_caso['clase_de_palabra_id']=list()
		dic_caso['lema_id']	=list()
		for caso in resultado:
			dic_caso['id'].append(caso.id)
			dic_caso['caso'].append(caso.caso)
			dic_caso['lema_anterior'].append(caso.lema_anterior)
			dic_caso['lema_posterior'].append(caso.lema_posterior)
			dic_caso['desinencia'].append(caso.desinencia)
			dic_caso['clase_de_palabra_id'].append(caso.clase_de_palabra_id)
			dic_caso['lema_id'].append(caso.lema_id)
		self.casos=pd.DataFrame(dic_caso)
		self.pre = pre
		self.pos = pos
		dic_docs={}
		dic_docs["id"]=[]
		dic_docs["zona_id"]=[]
		dic_docs["tema_id"]=[]
		dic_docs["subzona_id"]=[]
		dic_docs["provincia_id"]=[]
		for doc1 in doc:
			dic_docs["id"].append(doc1.id)
			dic_docs["zona_id"].append(doc1.zona_id)
			dic_docs["tema_id"].append(doc1.tema_id)
			dic_docs["subzona_id"].append(doc1.subzona_id)
			dic_docs["provincia_id"].append(doc1.provincia_id)
		self.doc = pd.DataFrame(dic_docs)
		self.doc = self.doc.drop_duplicates()
	def conteo_resultados(resultados):
		return len(resultados)
	def zoonificacion(self):
		zona_vc=self.doc['zona_id'].value_counts()
		zona_mas=zona_vc.idxmax()

		tfu = self.doc['tema_id'].value_counts().head(5)
		ax1= tfu.plot(kind='bar', xlabel='Temas', ylabel='Cantidad', rot=0)#, loc='upper left'
		flike1 = io.BytesIO()
		plt.savefig(flike1, bbox_inches="tight")
		temas_b64 = base64.b64encode(flike1.getvalue()).decode()
		try:
			plt.clf()
		except:
			pass

		dfu = self.doc.groupby(['zona_id'])["subzona_id"].value_counts().unstack()
		ax = dfu.plot(kind='bar', xlabel='Zonas', ylabel='Cantidad', rot=0).legend(title='Subzona', bbox_to_anchor=(1, 1))#, loc='upper left'
		flike = io.BytesIO()
		plt.savefig(flike, bbox_inches="tight")
		b64 = base64.b64encode(flike.getvalue()).decode()
		try:
			plt.clf()
		except:
			pass
		return zona_mas, b64, temas_b64
	def casificador(self):
		lemas_anteriores = self.casos['lema_anterior'].value_counts().head(5)
		lemas_posteriores = self.casos['lema_posterior'].value_counts().head(5)
		terminaciones = self.casos['desinencia'].value_counts().head(5)
		clases = self.casos['clase_de_palabra_id'].value_counts().head(5)
		lema = self.casos['lema_id'].value_counts().head(5)
		return lemas_anteriores.values, lemas_anteriores.index, lemas_posteriores.values, lemas_posteriores.index, terminaciones.values, terminaciones.index, clases.values, clases.index, lema.index
