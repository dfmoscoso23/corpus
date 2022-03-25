import pandas as pd
import io, base64
import matplotlib.pyplot as plt
from corpus_base.models import documentos, casos


class estadiador():

	def estadodocumentos():
		df = pd.DataFrame(list(documentos.objects.all().values()))
		cantidad_total= len(df["id"])

		dfu = df.groupby(['zona_id']).subzona_id.value_counts().unstack()
		ax = dfu.plot(kind='bar', xlabel='Zonas', ylabel='Cantidad', rot=0).legend(title='Subzona', bbox_to_anchor=(1, 1))#, loc='upper left'
		flike = io.BytesIO()
		plt.savefig(flike, bbox_inches="tight")
		b64 = base64.b64encode(flike.getvalue()).decode()
		try:
			plt.clf()
		except:
			pass

		tfu = df['tema_id'].value_counts()
		ax1= tfu.plot(kind='bar', xlabel='Temas', ylabel='Cantidad', rot=0)#, loc='upper left'
		flike1 = io.BytesIO()
		plt.savefig(flike1, bbox_inches="tight")
		temas_b64 = base64.b64encode(flike1.getvalue()).decode()
		try:
			plt.clf()
		except:
			pass

		vfu = df['tipo_documento_id'].value_counts()
		ax2= vfu.plot(kind='bar', xlabel='Temas', ylabel='Cantidad', rot=0)#, loc='upper left'
		flike2 = io.BytesIO()
		plt.savefig(flike2, bbox_inches="tight")
		tipo_b64 = base64.b64encode(flike2.getvalue()).decode()
		try:
			plt.clf()
		except:
			pass

		return cantidad_total, b64, temas_b64, tipo_b64
	def estadocasos():
		df_casos = pd.DataFrame(list(casos.objects.all().values()))
		cantidad_total= len(df_casos["id"])
		casos_unicos= len(df_casos['caso'].unique())
		cant_lemas = len(df_casos['lema_id'].unique())
		return cantidad_total, casos_unicos, cant_lemas