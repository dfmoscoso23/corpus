from django.contrib import admin
from django.urls import path
from autenticacion.views import VRegister
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', VRegister.as_view(), name="Register"),
    path('login/', LoginView.as_view(template_name='autenticacion/login.html'), name="Login"),
    path('logout/', LogoutView.as_view(template_name='autenticacion/logout.html'), name="Logout"),
]
