from django.conf.urls import url
from django.views.generic import TemplateView
from . import views


urlpatterns = [
	url(r'^paciente/$',views.registra_paciente, name='registra_paciente'),
	url(r'^paciente/(?P<paciente_pk>\d+)/domicilio/$',views.domicilio_paciente,name='domicilio_paciente'),
	url(r'^paciente/(?P<paciente_pk>\d+)/obstetrico/$',views.obstetrico_paciente,name='obstetrico_paciente'),
	url(r'^paciente/(?P<paciente_pk>\d+)/referencias/$',views.referencias_paciente,name='referencias_paciente'),
	url(r'^paciente/(?P<paciente_pk>\d+)/contrareferencias/$',views.contrareferencias_paciente,name='contrareferencias_paciente'),
	url(r'^paciente/(?P<paciente_pk>\d+)/tamizajes/$',views.tamizajes_paciente,name='tamizajes_paciente'),
	url(r'^busqueda/paciente/$',views.busqueda_paciente,name='busqueda_paciente'),
	url(r'^busqueda/generalpacientes/$', TemplateView.as_view(template_name='registro/busqueda_general_pacientes.html'),name='busqueda_general_pacientes'),
	url(r'^busqueda/tamizaje/$', TemplateView.as_view(template_name='registro/busqueda_tamizaje.html'),name='busqueda_tamizaje'),
	url(r'^busqueda/referencia/$', TemplateView.as_view(template_name='registro/busqueda_referencia.html'),name='busqueda_referencia'),
	url(r'^busqueda/contrareferencia/$', TemplateView.as_view(template_name='registro/busqueda_contrareferencia.html'),name='busqueda_contrareferencia'),
	
	
]