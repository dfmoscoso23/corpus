
from django.forms import ModelForm, Textarea, DateField,DateInput, TextInput
from corpus_base.models import documentos, casos, clases_de_palabras
from django.forms.widgets import NumberInput

class documentosForm(ModelForm):

	class Meta:
		model = documentos
		fields=["titulo","tipo_documento","fuente","fecha_publicacion","zona","subzona","tema","documento"]
		widgets = {
		"documento": Textarea(attrs={'cols':80,'rows':20}),
		"fecha_publicacion": NumberInput(attrs={'type': 'date'})#format='%d/%m/%Y'
		}
		#help_texts = {k:"" for k in fields}

class casosForm(ModelForm):

	class Meta:
		model = casos
		fields=["id","caso","lema","desinencia","prefijos","clase_de_palabra","determinante_1","determinante_2","determinante_3"]
		widgets = {
		'caso': Textarea(attrs={'rows':1,'cols':7}),
		'desinencia':Textarea(attrs={'rows':1,'cols':3}),
		'prefijos':Textarea(attrs={'rows':1,'cols':3})
		#'clase_de_palabra': Select(attrs={'onchange': 'load_determinante_1();'})
		# "documento": Textarea(attrs={'cols':80,'rows':20}),
		# "fecha_publicacion": DateInput(format='%d/%m/%Y')
		}
		#help_texts = {k:"" for k in fields}
		# print("chao")
		# def __init__(self, user, *args, **kwargs):
		# 	super(casosForm, self).__init__(*args, **kwargs)
		# 	 if self.data and self.data.get('clase_de_palabra'):
		# 		clase = clases_de_palabras.objects.get(clase=self.clase_de_palabra)
		# 		print(clase.determinante_1)
		# 		print("hola!")
		# 		self.fields['determinante_1'].queryset = determinante_1.objects.filter(tipo = clase.determinante_1)

class documentosfilterForm(ModelForm):

	class Meta:
		model =casos
		fields=["documento"]

class casosconsultaForm(ModelForm):

	class Meta:
		model = casos
		fields=["caso","lema","clase_de_palabra","determinante_1","determinante_2","determinante_3"]