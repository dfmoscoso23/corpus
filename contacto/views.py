from django.shortcuts import render, redirect
from .forms import ContactForm
# Create your views here.
def contacto(request):

	if request.method == "POST":
		formulario = ContactForm(data=request.POST)
		if formulario.is_valid():
			asunto=request.POST.get("asunto")
			mensaje=request.POST.get("mensaje")
			remitente=request.POST.get("remitente")
			copia=request.POST.get("copia")

			return redirect("/contacto/?valido")

	formulario = ContactForm()
	return render(request, "contacto/contacto.html",{"formulario_contacto":formulario})