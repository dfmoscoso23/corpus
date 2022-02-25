from django import forms

class ContactForm(forms.Form):
	asunto = forms.CharField(max_length=100,label="Asunto")
	mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje")
	remitente = forms.EmailField(label="Correo del remitente")
	copia = forms.BooleanField(required=False,label="Copia al remitente")