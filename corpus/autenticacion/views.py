from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from autenticacion.forms import UserRegisterForm, UserUpdateForm
from autenticacion.models import Profile
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
			form.save(commit=False)
			form.instance.is_active=False
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado. Próximamente recibirás un correo informando la aprobación de tu cuenta.')
			form.save()
			return redirect('Inicio')
		else:
			messages.success(request, f'El título ya existía'+str(form.errors))
			return render(request,"autenticacion/register.html",{"form":form})
		context= {'form': form}
		return render(request,"autenticacion/register.html", context)
class actualizarperfil(View):
	def get(self,request):
		if request.user.is_authenticated:
			current_user = request.user	
			insta=Profile.objects.get(user_id=current_user.id)	
			form=UserUpdateForm(instance=insta)
			usuario=current_user.username
			return render(request, "autenticacion/actualizarperfil.html",{
				"form":form,
				"usuario":usuario,
				"nombre":current_user.first_name,
				"apellido":current_user.last_name
				})
		else:
			messages.success(request, f'Debes estar registrado para acceder')
			return redirect("/")
	def post(self,request):
		if request.user.is_authenticated:
			current_user = request.user
			insta=Profile.objects.get(user_id=current_user.id)
			form=UserUpdateForm(request.POST or None, instance=insta)
			if form.is_valid():
				form.save(commit=False)
				form.instance.user_id=request.user.id
				messages.success(request, f'Usuario modificado')
				form.save()
				return redirect('Colaboradores')
			else:
				form = UserRegisterForm(request.POST or None, instance=current_user.id)
			context= {'form': form}
			return render(request,"autenticacion/actualizarperfil.html", context)
		else:
			messages.success(request, f'Debes estar registrado para acceder')
			return redirect("/")

