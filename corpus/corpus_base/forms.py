
from django.forms import ModelForm, Textarea, DateField,DateInput
from corpus_base.models import documentos, casos

class documentosForm(ModelForm):

	class Meta:
		model = documentos
		fields=["titulo","tipo_documento","fuente","fecha_publicacion","zona","subzona","tema","documento"]
		widgets = {
		"documento": Textarea(attrs={'cols':80,'rows':20}),
		"fecha_publicacion": DateInput()#format='%d/%m/%Y'
		}
		#help_texts = {k:"" for k in fields}

class casosForm(ModelForm):

	class Meta:
		model = casos
		fields=["id","caso","lema","desinencia","prefijos","clase_de_palabra","determinante_1","determinante_2","determinante_3"]
		# def __init__(self, user, *args, **kwargs):
		# 	super(casosForm, self).__init__(*args, **kwargs)
		# 	field_name = 'determinante_1'
		# 	obj = clases_de_palabras.objects.get(clase=self.c)
		# 	field_value = getattr(obj, field_name)
		# 	self.fields['determinante_1'].queryset = determinante_1.objects.filter(tipo = clases_de_palabras)
		# widgets = {
		# "documento": Textarea(attrs={'cols':80,'rows':20}),
		# "fecha_publicacion": DateInput(format='%d/%m/%Y')
		# }
		#help_texts = {k:"" for k in fields}

class documentosfilterForm(ModelForm):

	class Meta:
		model =casos
		fields=["documento"]

class casosconsultaForm(ModelForm):

	class Meta:
		model = casos
		fields=["caso","lema","clase_de_palabra","determinante_1","determinante_2","determinante_3"]