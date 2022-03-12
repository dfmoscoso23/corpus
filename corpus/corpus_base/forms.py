
from django.forms import ModelForm, Textarea, DateField,DateInput, TextInput, Form,ChoiceField, Select, CharField
from corpus_base.models import documentos, casos, clases_de_palabras, zonas, subzonas
from django.forms.widgets import NumberInput
import json

class documentosForm(ModelForm):

	class Meta:
		model = documentos
		fields=["titulo","tipo_documento","fuente","autor","referencia_específica","fecha_publicacion","zona","subzona","tema","documento"]
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

# class casosconsultaForm(ModelForm):

# 	class Meta:
# 		model = casos
# 		fields=["caso","lema","clase_de_palabra"]
# 		widgets = {
# 		'caso': Textarea(attrs={'rows':1,'cols':7}),
# 		'lema':Textarea(attrs={'rows':1,'cols':3})
# 		}

class FormularioZonas(Form):
	zonas_form = ChoiceField(label="Zonas:", choices=(), widget=Select(attrs={'class':'form-control'}))
	subzonas_form = ChoiceField(label="subZonas:", choices=(), widget=Select(attrs={'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		EXTRA_CHOICES = [(10,'Todas')]
		super(FormularioZonas, self).__init__(*args, **kwargs)
		choices = EXTRA_CHOICES.copy()
		choices.extend([(pt.id,pt.zona) for pt in zonas.objects.all()])
		self.fields['zonas_form'].choices = choices
		choices_sub = EXTRA_CHOICES.copy()
		choices_sub.extend([(int(pt.id),pt.subzona) for pt in subzonas.objects.all()])
		self.fields['subzonas_form'].choices=choices_sub
		self.fields['subzonas_form'].required = False
		self.fields['zonas_form'].required = False
		# if 'zona_id' in self.data:
		# 	print("AJJAJAAJAJ")
		# 	#try:
		# 	print(self.data)
		# 	zona_id = int(self.data.get('zona_id'))
		# 	print(zona_id)
		# 	zona=zonas.objects.filter(id=zona_id)
		# 	print(zona[0])
		# 	print(subzonas.objects.filter(zona=zona[0]))
		# 	choices_sub=[(pt.id,pt.subzona) for pt in subzonas.objects.filter(zona=zona[0])]
		# 	print(choices_sub)
		# 	choices_sub.extend(EXTRA_CHOICES)
		# 	self.fields['subzonas_form'].choices=choices_sub
		# 	#except:
		# 		#pass
		# else:
		# 	self.fields['subzonas_form'].choices =[]

def formasConsultaForm(Form):
	forma_exacta = CharField(label="Forma Exacta:")
	forma_aproximada = CharField(label="Forma Exacta:")
	lema = CharField(label="Lema:")
	clase = ChoiceField(label="Zonas:", choices=clases_de_palabras.objects.all(), widget=Select(attrs={'class':'form-control'}))