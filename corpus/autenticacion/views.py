from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from autenticacion.forms import UserRegisterForm
# Create your views here.
# def autenticacion(request):

# 	return render(request, "autenticacion/login.html")

class VRegister(View):

	def get(self,request):
		form=UserRegisterForm()
		return render(request, "autenticacion/register.html",{"form":form})
	def post(self,request):
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			form.save()
			return redirect('Logout')
		else:
			form = UserRegisterForm()
		context= {'form': form}
		return render(request,"autenticacion/register.html", context)