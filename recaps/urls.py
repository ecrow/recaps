"""recaps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^registro/',include('registro.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url(r'^logout_login/$', 'django.contrib.auth.views.logout_then_login'),
    
    url(r'^catalogo/estado/$',views.catalogo_estado),
    url(r'^catalogo/municipio/$',views.catalogo_municipio),
    url(r'^catalogo/localidad/$',views.catalogo_localidad),
    url(r'^catalogo/tipo_tamizaje/$',views.catalogo_tipo_tamizaje),
    url(r'^catalogo/tipo_tratamiento/$',views.catalogo_tipo_tratamiento),
    url(r'^catalogo/resultado/$',views.catalogo_resultado),
    url(r'^catalogo/unidad/$',views.catalogo_unidad),
    url(r'^catalogo/cs/$',views.catalogo_cs),
    url(r'^catalogo/hosp/$',views.catalogo_hosp),

    url(r'^calcula/sg/$',views.calcula_sg),
    url(r'^calcula/fum/$',views.calcula_fum),

    url(r'^busqueda/js/pacientes/$',views.busqueda_js_pacientes,name='busqueda_js_pacientes'),
    url(r'^busqueda/js/tamizaje/$',views.busqueda_js_tamizaje,name='busqueda_js_tamizaje'),
    url(r'^busqueda/js/referencia/$',views.busqueda_js_referencia,name='busqueda_js_referencia'),
    url(r'^busqueda/js/contrareferencia/$',views.busqueda_js_contrareferencia,name='busqueda_js_contrareferencia'),

    url(r'^tamizaje/(?P<elemento_id>\d+)/borra/$',views.borra_tamizaje,name='borra_tamizaje'),
    url(r'^referencia/(?P<elemento_id>\d+)/borra/$',views.borra_referencia,name='borra_referencia'),
    url(r'^contrareferencia/(?P<elemento_id>\d+)/borra/$',views.borra_contrareferencia,name='borra_contrareferencia'),

]


urlpatterns +=staticfiles_urlpatterns()
