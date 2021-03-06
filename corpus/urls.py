"""corpus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from corpus_base import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="Inicio"),
    path('documentos/', views.documentos, name="Documentos"),
    path('documento/', views.documento_ficha, name="Documento"),
    path('consulta/', views.consulta, name="Consulta"),
    path('consulta/resultado', views.resultado, name="Resultado"),
    #path('consulta/resultado/estadisticas', views.estadisticas, name="Estadisticas"),
    path('contacto/', include('contacto.urls')),
    path('acercade/', include('acercade.urls')),
    path('procesando/', views.procesando, name="Procesando"),
    path('autenticacion/', include('autenticacion.urls')),
    path('corregir/', views.correccion, name="Correccion"),
    path('ajax/load-subzonas/', views.load_subzonas, name="ajax_load_zonas"),
    path('ajax/load-determinantes/', views.load_determinantes, name="ajax_load_clases"),
    path('articulos/', include('articulos.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
