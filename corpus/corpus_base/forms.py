
from django.forms import ModelForm, Textarea, DateField,DateInput
from corpus_base.models import documentos

class documentosForm(ModelForm):

	class Meta:
		model = documentos
		fields=["titulo","tipo_documento","fuente","fecha_publicacion","zona","subzona","tema","documento"]
		widgets = {
		"documento": Textarea(attrs={'cols':80,'rows':20}),
		"fecha_publicacion": DateInput(format='%d/%m/%Y')
		}
		#help_texts = {k:"" for k in fields}