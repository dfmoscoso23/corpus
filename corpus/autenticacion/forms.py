from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
	#user = forms.CharField(label="Usuario")
	email = forms.EmailField(label="Correo electrónico")
	password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirma Contraseña", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields=["username","email","password1"]
		help_texts = {k:"" for k in fields}