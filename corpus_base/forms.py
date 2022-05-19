
from django.forms import ModelForm, Textarea, DateField,DateInput, TextInput, Form,ChoiceField, Select, CharField, TypedChoiceField
from corpus_base.models import documentos, casos, clases_de_palabras, zonas, subzonas, tipo_documento
from django.forms.widgets import NumberInput

class documentosForm(ModelForm):

	class Meta:
		model = documentos
		fields=["titulo","tipo_documento","fuente","autor","referencia_específica","fecha_publicacion","zona","subzona","provincia","tema","documento"]
		widgets = {
		"documento": Textarea(attrs={'cols':80,'rows':25}),
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

class documentosfilterForm(ModelForm):

	class Meta:
		model =casos
		fields=["documento"]


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

def formasConsultaForm(Form):
	forma_exacta = CharField(label="Forma Exacta:")
	forma_aproximada = CharField(label="Forma Exacta:")
	lema = CharField(label="Lema:")
	clase = ChoiceField(label="Zonas:", choices=clases_de_palabras.objects.all(), widget=Select(attrs={'class':'form-control'}))

class tiposForm(ModelForm):

	class Meta:
		model = documentos
		fields=["tipo_documento","revisado"]
	def __init__(self, *args, **kwargs):
		super(tiposForm, self).__init__(*args, **kwargs)
		self.fields['tipo_documento'].required = False

def yearForm(Form):
	preyear = ChoiceField(label="Desde:", choices=(), widget=Select(attrs={'class':'form-control'}))
	posyear = ChoiceField(label="Hasta:", choices=(), widget=Select(attrs={'class':'form-control'}))
	def __init__(self, *args, **kwargs):
		EXTRA_CHOICES = [(0,'Todas')]
		super(yearForm, self).__init__(*args, **kwargs)
		first_year = documentos.objects.order_by('fecha_publicacion').first()
		last_year=documentos.objects.order_by('fecha_publicacion').last()
		print(first_year.fecha_publicacion.year)
		print(type(first_year.fecha_publicacion.year))
		rango=[(z) for z in range(first_year.fecha_publicacion.year,last_year.fecha_publicacion.year+1)]
		print(rango)
		self.fields['preyear'].required = False
		self.fields['posyear'].required = False
