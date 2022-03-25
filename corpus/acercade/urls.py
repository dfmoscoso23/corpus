from django.contrib import admin
from django.urls import path
from acercade import views

urlpatterns = [
    path('', views.acercade, name="Acercade"),
    path('colaboradores/', views.colaboradores, name="Colaboradores"),
    path('estado/', views.estado, name="Estado"),
]
