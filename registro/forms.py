from django import forms
from . import models


class PacienteForm(forms.Form):
	fnombre = forms.CharField(max_length=100)
	fapaterno = forms.CharField(max_length=50)
	famaterno = forms.CharField(max_length=50,required=False)
	fedad = forms.IntegerField(required=False)
	funidad = forms.IntegerField()
	
class DomicilioForm(forms.Form):
	flocalidad = forms.IntegerField()
	fdomicilio = forms.CharField(required=False)
	ftelefono=forms.CharField(max_length=10,required=False)
	
class ObstetricoForm(forms.Form):
	ffum = forms.DateTimeField(input_formats=['%d/%m/%Y',])
	fultra = forms.BooleanField(required=False)
	fngesta = forms.IntegerField()
	ffactores = forms.CharField(required=False)


class ReferenciaForm(forms.Form):
	ftipo_tamizaje = forms.IntegerField()
	funidad_refiere = forms.IntegerField()
	funidad_recibe = forms.IntegerField()
	ffecha_envio = forms.DateTimeField(input_formats=['%d/%m/%Y',])
	fobservaciones = forms.CharField(required=False)


class ContrareferenciaForm(forms.Form):
	funidad_contrarefiere = forms.IntegerField()
	funidad_recibe = forms.IntegerField()
	ffecha_envio = forms.DateTimeField(input_formats=['%d/%m/%Y',])
	fobservaciones = forms.CharField(required=False)


class TamizajeForm(forms.Form):
	ffecha_consulta = forms.DateTimeField(input_formats=['%d/%m/%Y',])
	funidad_realiza = forms.IntegerField()
	ftipo_tamizaje = forms.IntegerField()
	fresultado = forms.IntegerField()
	ftipo_tratamiento = forms.IntegerField()