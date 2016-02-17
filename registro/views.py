#encoding:utf-8
import datetime
import operator

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from .models import *
from .forms import PacienteForm
from .forms import DomicilioForm
from .forms import ObstetricoForm
from .forms import ReferenciaForm
from .forms import ContrareferenciaForm
from .forms import TamizajeForm
from .objetos import *



@login_required
def registra_paciente(request): 

	if request.method == 'POST':
		form = PacienteForm(request.POST)
		if form.is_valid():
		
			try:
				
				nombre = form.cleaned_data['fnombre']
				apaterno = form.cleaned_data['fapaterno']
				amaterno = form.cleaned_data['famaterno']
				edad = form.cleaned_data['fedad']
				unidad = form.cleaned_data['funidad']
				usuario_registro = request.user
				fecha_registro = timezone.now()

				unidadObjeto = Unidad.objects.get(pk=unidad, status='A')

				paciente = Paciente.objects.create(
					nombre=nombre.upper(),
					apellido_paterno=apaterno.upper(),
					apellido_materno=amaterno.upper(),
					edad = edad,
					unidad = unidadObjeto,
					usuario_registro=usuario_registro,
					fecha_registro=fecha_registro
				)

				return HttpResponseRedirect(reverse('domicilio_paciente',kwargs={'paciente_pk':paciente.id}))

			except Exception, e:
				return render(request,'registro/registra_paciente.html',{'error': e.message})

		else:
			return render(request,'registro/registra_paciente.html',{'error': form.errors})

	return render(request,'registro/registra_paciente.html',{})

@login_required
def domicilio_paciente(request,paciente_pk):

	paciente = get_object_or_404(Paciente,pk=paciente_pk)	
	diccionario = {'paciente':paciente}

	try:
		domicilio = Domicilio.objects.get(paciente = paciente, status='A')
		diccionario['domicilio'] = domicilio
	except ObjectDoesNotExist:
		diccionario['domicilio'] = None
		

	if request.method == 'POST':
		form = DomicilioForm(request.POST)
		if form.is_valid():
			try:
				localidad = form.cleaned_data['flocalidad']
				calle = form.cleaned_data['fdomicilio']
				telefono = form.cleaned_data['ftelefono']

				localidadObjeto = Localidad.objects.get(pk=localidad, status='A')

				domicilio = Domicilio.objects.create(
					paciente = paciente,
					localidad = localidadObjeto,
					domicilio = calle,
					telefono = telefono,
					usuario_registro=request.user,
					fecha_registro=timezone.now()
				)

				diccionario['domicilio'] = domicilio
				return render(request,'registro/domicilio_paciente.html', diccionario)	

			except Exception, e:
				diccionario['error'] = e.message
				return render(request,'registro/domicilio_paciente.html', diccionario)
		else:
			diccionario['error'] = form.errors
			return render(request,'registro/domicilio_paciente.html', diccionario)

	return render(request,'registro/domicilio_paciente.html', diccionario)	

@login_required
def obstetrico_paciente(request,paciente_pk):
	paciente = get_object_or_404(Paciente,pk=paciente_pk)
	diccionario = {'paciente':paciente}

	try:
		obstetrico = Obstetrico.objects.get(paciente = paciente, status='A')
		diccionario['obstetrico'] = obstetrico
	except ObjectDoesNotExist:
		diccionario['obstetrico'] = None

	if request.method == 'POST':
		form = ObstetricoForm(request.POST)
		if form.is_valid():
			try:
				fum = form.cleaned_data['ffum']
				factores = form.cleaned_data['ffactores']
				numero_gesta = form.cleaned_data['fngesta']
				ultrasonido = 'fultra' in request.POST

				obstetrico = Obstetrico.objects.create(
					paciente = paciente,
					fum = fum,
					factores_riesgo = factores,
					gesta = numero_gesta,
					ultrasonido = ultrasonido,
					usuario_registro=request.user,
					fecha_registro=timezone.now()
				)

				diccionario['obstetrico'] = obstetrico
				return render(request,'registro/obstetrico_paciente.html',diccionario)	

			except Exception, e:
				diccionario['error'] = e.message
				return render(request,'registro/obstetrico_paciente.html',diccionario)	
		else:
			diccionario['error'] = form.errors
			return render(request,'registro/obstetrico_paciente.html', diccionario)	


	return render(request,'registro/obstetrico_paciente.html',diccionario)	


@login_required
def referencias_paciente(request, paciente_pk):
	paciente = get_object_or_404(Paciente,pk=paciente_pk)
	referencias = Referencia.objects.filter(paciente = paciente, status='A')

	diccionario = {'paciente':paciente,'referencias':referencias}
	if request.method == 'POST':
		form = ReferenciaForm(request.POST)
		if form.is_valid():
			try:
				tipo_tamizaje = form.cleaned_data['ftipo_tamizaje']
				unidad_refiere = form.cleaned_data['funidad_refiere']
				unidad_recibe = form.cleaned_data['funidad_recibe']
				fecha_envio = form.cleaned_data['ffecha_envio']
				observaciones = form.cleaned_data['fobservaciones']

				tipo_tamizajeObject = Tipo_Tamizaje.objects.get(pk=tipo_tamizaje,status='A')
				unidad_refiereObject = Unidad.objects.get(pk=unidad_refiere,status='A')
				unidad_recibeObject = Unidad.objects.get(pk=unidad_recibe,status='A')

				referencia = Referencia.objects.create(
					paciente = paciente,
					tipo_tamizaje = tipo_tamizajeObject,
					unidad_refiere = unidad_refiereObject,
					unidad_recibe = unidad_recibeObject,
					fecha_envio = fecha_envio,
					observaciones = observaciones,
					usuario_registro=request.user,
					fecha_registro=timezone.now()
				)
				#return render(request,'registro/referencias_paciente.html',{})	
				return HttpResponseRedirect(reverse('referencias_paciente',kwargs={'paciente_pk':paciente.id}))

			except Exception, e:
				diccionario['error'] = e.message
				return render(request,'registro/referencias_paciente.html',diccionario)
		else:
			diccionario['error'] = form.errors
			return render(request,'registro/referencias_paciente.html',diccionario)

	return render(request,'registro/referencias_paciente.html',diccionario)

@login_required
def contrareferencias_paciente(request, paciente_pk):
	paciente = get_object_or_404(Paciente,pk=paciente_pk)
	contrareferencias = Contrareferencia.objects.filter(paciente = paciente, status='A')

	diccionario = {'paciente':paciente,'contrareferencias':contrareferencias}
	if request.method == 'POST':
		form = ContrareferenciaForm(request.POST)
		if form.is_valid():
			try:
				
				unidad_contrarefiere = form.cleaned_data['funidad_contrarefiere']
				unidad_recibe = form.cleaned_data['funidad_recibe']
				fecha_envio = form.cleaned_data['ffecha_envio']
				observaciones = form.cleaned_data['fobservaciones']

				
				unidad_contrarefiereObject = Unidad.objects.get(pk=unidad_contrarefiere,status='A')
				unidad_recibeObject = Unidad.objects.get(pk=unidad_recibe,status='A')

				contrareferencia = Contrareferencia.objects.create(
					paciente = paciente,
					unidad_contrarefiere = unidad_contrarefiereObject,
					unidad_recibe = unidad_recibeObject,
					fecha_envio = fecha_envio,
					observaciones = observaciones,
					usuario_registro=request.user,
					fecha_registro=timezone.now()
				)
				return HttpResponseRedirect(reverse('contrareferencias_paciente',kwargs={'paciente_pk':paciente.id}))
				

			except Exception, e:
				diccionario['error'] = e.message
				return render(request,'registro/contrareferencias_paciente.html',diccionario)
		else:
			diccionario['error'] = form.errors
			return render(request,'registro/contrareferencias_paciente.html',diccionario)

	return render(request,'registro/contrareferencias_paciente.html',diccionario)


@login_required
def tamizajes_paciente(request, paciente_pk):

	paciente = get_object_or_404(Paciente,pk=paciente_pk)

	try:
		obstetrico = Obstetrico.objects.get(paciente = paciente, status='A')
	except ObjectDoesNotExist:
		obstetrico = None
	
	tamizajes = []

	for tamizaje in Tamizaje.objects.filter(paciente = paciente, status='A'):
		custom_tamizaje = Custom_tamizaje()
		custom_tamizaje.id=tamizaje.id
		custom_tamizaje.fecha_consulta = tamizaje.fecha_consulta
		custom_tamizaje.unidad_realiza = tamizaje.unidad_realiza
		custom_tamizaje.tipo_tamizaje = tamizaje.tipo_tamizaje
		custom_tamizaje.resultado = tamizaje.resultado
		custom_tamizaje.tipo_tratamiento = tamizaje.tipo_tratamiento
		custom_tamizaje.fecha_registro=tamizaje.fecha_registro

		if obstetrico:
			semanas = (tamizaje.fecha_consulta - obstetrico.fum).days / 7
			dias = (tamizaje.fecha_consulta - obstetrico.fum).days % 7
			semanas_de_gestacion = str(semanas)+'.'+str(dias) 
			custom_tamizaje.sg_fecha_consulta = semanas_de_gestacion

		tamizajes.append(custom_tamizaje)

	diccionario = {'paciente':paciente,'tamizajes':tamizajes}

	if request.method == 'POST':
		form = TamizajeForm(request.POST)
		if form.is_valid():
			try:
				fecha_consulta = form.cleaned_data['ffecha_consulta']
				tipo_tamizaje = form.cleaned_data['ftipo_tamizaje']
				unidad_realiza = form.cleaned_data['funidad_realiza']
				resultado = form.cleaned_data['fresultado']
				tipo_tratamiento = form.cleaned_data['ftipo_tratamiento']

				
				tipo_tamizajeObject = Tipo_Tamizaje.objects.get(pk=tipo_tamizaje,status='A')
				tipo_tratamientoObject = Tipo_Tratamiento.objects.get(pk=tipo_tratamiento,status='A')
				resultadoObject = Resultado.objects.get(pk=resultado, status='A')
				unidad_realizaObject = Unidad.objects.get(pk=unidad_realiza,status='A')

				tamizaje = Tamizaje.objects.create(
					paciente = paciente,
					fecha_consulta = fecha_consulta,
					unidad_realiza = unidad_realizaObject,
					tipo_tamizaje = tipo_tamizajeObject,
					resultado = resultadoObject,
					tipo_tratamiento = tipo_tratamientoObject,
					usuario_registro=request.user,
					fecha_registro=timezone.now()
				)
				return HttpResponseRedirect(reverse('tamizajes_paciente',kwargs={'paciente_pk':paciente.id}))

			except Exception, e:
				diccionario['error'] = e.message
				return render(request,'registro/tamizajes_paciente.html',diccionario)
		else:
			diccionario['error'] = form.errors
			return render(request,'registro/tamizajes_paciente.html',diccionario)

	return render(request,'registro/tamizajes_paciente.html',diccionario)



@login_required
def busqueda_paciente(request):
	try:
		query_strings=request.GET.keys()
		if query_strings:
			page = request.GET.get('page')
			predicados = []
			if 'busqueda_paciente' in request.GET:
				paciente_nombre=request.GET['busqueda_paciente']

				for term in paciente_nombre.split():
					#pacientes = pacientes.filter(Q(nombre__icontains = term) | Q(apellido_paterno__icontains = term) | Q(apellido_materno__icontains = term))
					predicados.append(('nombre__icontains',term))
					predicados.append(('apellido_paterno__icontains',term))
					predicados.append(('apellido_materno__icontains',term))

			if predicados:
				request.session['predicados']= list(predicados)
				q_list = [Q(x) for x in predicados]
				pacientes = Paciente.objects.filter(reduce(operator.or_, q_list),status='A').order_by('-fecha_registro')
			else:
				if 'predicados' in request.session:
					predicados=request.session['predicados']
					if predicados and page:
						q_list = [Q(x) for x in predicados]
						pacientes = Paciente.objects.filter(reduce(operator.or_, q_list),status='A').order_by('-fecha_registro')
					else:
						del request.session['predicados']
						pacientes=Paciente.objects.filter(status='A').order_by('-fecha_registro')

				else:
					pacientes=Paciente.objects.filter(status='A').order_by('-fecha_registro')
		
		else:
			if 'predicados' in request.session:
				del request.session['predicados']
			pacientes=Paciente.objects.filter(status='A').order_by('-fecha_registro')
			page=1

		paginator = Paginator(pacientes, 10)
		try:
			patients = paginator.page(page)
		except PageNotAnInteger:
			patients = paginator.page(1)
		except EmptyPage:
			patients = paginator.page(paginator.num_pages)

		dictionary={
			'pacientes':pacientes,
			'patients':patients,
			'paginator':paginator,
			}

		if pacientes:
			return render(request,'registro/busqueda_pacientes.html',dictionary)
		else:
			return render(request,'registro/busqueda_pacientes.html',{'msg':'El criterio de búsqueda no encontro resultados'})
				
	except Exception, e:
		return render(request,'registro/error.html',{'error':e.message})


