from django.contrib import admin
from django.urls import path
from articulos import views

urlpatterns = [
    path('', views.articulos, name="Articulos"),
    path('articulo/', views.articulo_desplegado, name="ArticuloDesplegado"),
]
