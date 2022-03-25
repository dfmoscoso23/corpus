from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from autenticacion.models import Profile
from corpus_base.models import subzonas

class UserRegisterForm(UserCreationForm):
	#user = forms.CharField(label="Usuario")
	email = forms.EmailField(label="Correo electrónico")
	password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirma Contraseña", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields=["username","email","password1","first_name","last_name"]
		help_texts = {k:"" for k in fields}
		labels = {
			"first_name": "Nombre:",
			"last_name": "Apellido:"
		}

class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields=["location","birthdate","role","bio"]
		help_texts = {k:"" for k in fields}
		labels = {
			"bio": "Biografía:",
			"location": "Lugar de Residencia:",
			"birthdate": "Fecha de nacimiento:",
			"role": "Nivel de estudios:"
		}
		widgets = {
		"bio": forms.Textarea(attrs={'cols':80,'rows':3}),
		"birthdate": forms.NumberInput(attrs={'type': 'date'}),#format='%d/%m/%Y'
		# "location": forms.Select(choices=)
		}