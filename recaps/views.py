#encoding:utf-8
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.core.urlresolvers import reverse
from registro.models import *
from django.db.models import Q
import datetime
import operator

@login_required
def index(request):
	return render(request,'index.html')

@login_required
def catalogo_estado(request):
	lista_estado = []
	for estado in Estado.objects.filter(status='A').order_by('id'):
		lista_estado.append({'estado_id': estado.id,'descripcion': estado.descripcion})
	return JsonResponse(lista_estado,safe=False)


@login_required
def catalogo_municipio(request):
	lista_municipio = []
	for municipio in Municipio.objects.filter(status='A').order_by('id'):
		lista_municipio.append({
			'municipio_id': municipio.id,
			'estado_id':municipio.estado.id,
			'descripcion': municipio.clave+'-'+municipio.descripcion
		})
	return JsonResponse(lista_municipio,safe=False)


@login_required
def catalogo_localidad(request):
	lista_localidad = []
	for localidad in Localidad.objects.filter(status='A').order_by('id'):
		lista_localidad.append({
			'localidad_id':localidad.id,
			'municipio_id':localidad.municipio.id,
			'estado_id':localidad.municipio.estado.id,
			'descripcion': localidad.clave+'-'+localidad.descripcion
		})
	return JsonResponse(lista_localidad,safe=False)


@login_required
def catalogo_tipo_tamizaje(request):
	lista_tipo_tamizaje = []
	for tipo_tamizaje in Tipo_Tamizaje.objects.filter(status='A'):
		lista_tipo_tamizaje.append({
			'tipo_tamizaje_id': tipo_tamizaje.id,
			'descripcion':tipo_tamizaje.descripcion
		})
	return JsonResponse(lista_tipo_tamizaje,safe=False)

@login_required
def catalogo_unidad(request):

	if request.user.is_staff or  request.user.groups.filter(name='hospitales').exists() or request.user.groups.filter(name='supervisores').exists():

		unidades = 	Unidad.objects.filter(status='A')	
	else:
		unidades = Unidad.objects.filter(status='A', usuario_unidad__usuario=request.user, usuario_unidad__status='A')
		
	lista_unidad = []
	for unidad in unidades:
		lista_unidad.append({
			'unidad_id':unidad.id,
			'descripcion':unidad.descripcion
		})
	return JsonResponse(lista_unidad,safe=False)

@login_required
def catalogo_tipo_tratamiento(request):
	lista_tipo_tratamiento = []
	for tipo_tratamiento in Tipo_Tratamiento.objects.filter(status='A'):
		lista_tipo_tratamiento.append({
			'tipo_tratamiento_id':tipo_tratamiento.id,
			'descripcion':tipo_tratamiento.descripcion
		})
	return JsonResponse(lista_tipo_tratamiento,safe=False)


@login_required
def catalogo_resultado(request):
	lista_resultado = []
	for resultado in Resultado.objects.filter(status='A'):
		lista_resultado.append({
			'resultado_id':resultado.id,
			'descripcion':resultado.descripcion
		})
	return JsonResponse(lista_resultado,safe=False)


@login_required
def calcula_sg(request):
	if request.method=='POST':
		try:
			fum = datetime.datetime.strptime(request.POST['fum'], '%d/%m/%Y')
			semanas = (datetime.datetime.now() - fum).days / 7
			dias = (datetime.datetime.now() - fum).days % 7
			semanas_de_gestacion = str(semanas)+'.'+str(dias) 

			fpp = fum + datetime.timedelta(days=277)
			fpp = fpp.strftime('%d/%m/%Y')

			return JsonResponse(
				{
					'status':'1',
					'msg' : 'success',
					'sg':semanas_de_gestacion,
					'fpp':fpp
				},
				safe=False)

		except Exception, e:
			return JsonResponse({'status':'0','msg' : e.message},safe=False)			

	return JsonResponse({'status':'0','msg' : 'Bad request'},safe=False)			


@login_required
def calcula_fum(request):
	if request.method=='POST':
		try:
			semanas_de_gestacion = float(request.POST['sg'])
			semanas = int(semanas_de_gestacion)
			dias_sobrantes = (semanas_de_gestacion - semanas) * 10
			dias = (semanas * 7) + dias_sobrantes

			fum = datetime.datetime.now() - datetime.timedelta(days=dias)
			fpp = fum + datetime.timedelta(days=277)

			fum = fum.strftime('%d/%m/%Y')
			fpp = fpp.strftime('%d/%m/%Y')

			return JsonResponse(
				{
					'status':'1',
					'msg' : 'success',
					'fum':fum,
					'fpp':fpp
				},
				safe=False)

		except Exception , e:
			return JsonResponse({'status':'0','msg' : e.message},safe=False)	

	return JsonResponse({'status':'0','msg' : 'Bad request'},safe=False)	

@login_required
def busqueda_js_tamizaje(request):
	try:
		if request.method=='GET':
			lista_resultado_busqueda = []
			query_strings=request.GET.keys()
			if query_strings:
				predicados=[]

				fecha_inicial=request.GET['fecha_ini']
				fecha_final=request.GET['fecha_fin']

				if 'valor_range' in request.GET.keys():
					valor_range = request.GET['valor_range']
					if valor_range:
						rango_edad = [int(edad) for edad in valor_range.split(',')]
						predicados.append(('paciente__edad__range',rango_edad))

				if fecha_inicial and fecha_final:
					fecha_inicial=datetime.datetime.strptime(fecha_inicial,'%d/%m/%Y')
					fecha_final=datetime.datetime.strptime(fecha_final,'%d/%m/%Y').replace(hour=23,minute=59)
					predicados.append(('fecha_consulta__range',(fecha_inicial,fecha_final)))
				else:
					fecha_inicial=datetime.datetime.strptime('01/01/2000','%d/%m/%Y')
					fecha_final=timezone.now().replace(hour=23,minute=59)
					predicados.append(('fecha_consulta__range',(fecha_inicial,fecha_final)))

				if 'unidad_realiza' in request.GET:
					unidad_realiza=request.GET['unidad_realiza']
					if unidad_realiza:
						predicados.append(('unidad_realiza__id',unidad_realiza))

				if 'tipo_tamizaje' in request.GET:
					tipo_tamizaje=request.GET['tipo_tamizaje']
					if tipo_tamizaje:
						predicados.append(('tipo_tamizaje__id',tipo_tamizaje))

				if 'resultado' in request.GET:
					resultado=request.GET['resultado']
					if resultado:
						predicados.append(('resultado__id',resultado))

				if 'tratamiento' in request.GET:
					tratamiento=request.GET['tratamiento']
					if tratamiento:
						predicados.append(('tipo_tratamiento__id',tratamiento))

				q_list = [Q(x) for x in predicados]
				tamizajes=Tamizaje.objects.filter(reduce(operator.and_, q_list))

				
				for tamizaje in tamizajes:
					lista_resultado_busqueda.append({
						'fecha_consulta':tamizaje.fecha_consulta,
						'tipo_tamizaje':tamizaje.tipo_tamizaje.descripcion,
						'unidad_realiza':tamizaje.unidad_realiza.descripcion,
						'resultado':tamizaje.resultado.descripcion,
						'tipo_tratamiento':tamizaje.tipo_tratamiento.descripcion,
						'url':reverse('tamizajes_paciente',kwargs={'paciente_pk':tamizaje.paciente.id}),
						'edad_paciente': tamizaje.paciente.edad,
					})

				return JsonResponse(lista_resultado_busqueda,safe=False)
				
			else:
				return JsonResponse(lista_resultado_busqueda,safe=False)
	except Exception, e:
		return render(request,'registro/error.html',{'error':e.message})

@login_required
def busqueda_js_pacientes(request):
	try:
		if request.method=='GET':
			lista_resultado_busqueda = []
			query_strings=request.GET.keys()
			if query_strings:
				predicados=[]

				if 'valor_range' in request.GET.keys():
					valor_range = request.GET['valor_range']
					if valor_range:
						rango_edad = [int(edad) for edad in valor_range.split(',')]
						predicados.append(('edad__range',rango_edad))

				if 'unidad_paciente' in request.GET:
					unidad_paciente=request.GET['unidad_paciente']
					if unidad_paciente:
						predicados.append(('unidad__id',unidad_paciente))

				if predicados:
					q_list = [Q(x) for x in predicados]
					pacientes=Paciente.objects.filter(reduce(operator.and_, q_list))
				else:
					pacientes=Paciente.objects.filter(status='A').order_by('-fecha_registro')

				domicilio_completo = ''
				for paciente in pacientes:

					try:
						domicilio = Domicilio.objects.get(paciente = paciente, status='A')
						domicilio_completo = domicilio.get_domicilio_completo()
					except ObjectDoesNotExist:
						domicilio_completo=''

					nombre = u'{} {} {}'.format(paciente.nombre,paciente.apellido_paterno,paciente.apellido_materno)
					lista_resultado_busqueda.append({
						'nombre':nombre,
						'domicilio':domicilio_completo,
						'url':reverse('domicilio_paciente',kwargs={'paciente_pk':paciente.id}),
						'unidad_paciente': paciente.unidad.descripcion,
						'edad_paciente': paciente.edad,
					})

				print lista_resultado_busqueda
				return JsonResponse(lista_resultado_busqueda,safe=False)
				
			else:
				return JsonResponse(lista_resultado_busqueda,safe=False)
	except Exception, e:
		return render(request,'registro/error.html',{'error':e.message})


@login_required
def busqueda_js_referencia(request):
	try:
		if request.method=='GET':
			lista_resultado_busqueda = []
			query_strings=request.GET.keys()
			if query_strings:
				predicados=[]

				fecha_inicial=request.GET['fecha_ini']
				fecha_final=request.GET['fecha_fin']

				if fecha_inicial and fecha_final:
					fecha_inicial=datetime.datetime.strptime(fecha_inicial,'%d/%m/%Y')
					fecha_final=datetime.datetime.strptime(fecha_final,'%d/%m/%Y').replace(hour=23,minute=59)
					predicados.append(('fecha_envio__range',(fecha_inicial,fecha_final)))
				else:
					fecha_inicial=datetime.datetime.strptime('01/01/2000','%d/%m/%Y')
					fecha_final=timezone.now().replace(hour=23,minute=59)
					predicados.append(('fecha_envio__range',(fecha_inicial,fecha_final)))

				if 'unidad_refiere' in request.GET:
					unidad_refiere=request.GET['unidad_refiere']
					if unidad_refiere:
						predicados.append(('unidad_refiere__id',unidad_refiere))

				if 'unidad_recibe' in request.GET:
					unidad_recibe=request.GET['unidad_recibe']
					if unidad_recibe:
						predicados.append(('unidad_recibe__id',unidad_recibe))

				if 'tipo_tamizaje' in request.GET:
					tipo_tamizaje=request.GET['tipo_tamizaje']
					if tipo_tamizaje:
						predicados.append(('tipo_tamizaje__id',tipo_tamizaje))

				q_list = [Q(x) for x in predicados]
				referencias=Referencia.objects.filter(reduce(operator.and_, q_list))

				
				for referencia in referencias:
					lista_resultado_busqueda.append({
						'url':reverse('referencias_paciente',kwargs={'paciente_pk':referencia.paciente.id}),
						'fecha_envio':referencia.fecha_envio,
						'unidad_refiere':referencia.unidad_refiere.descripcion,
						'unidad_recibe':referencia.unidad_recibe.descripcion,
						'tipo_tamizaje':referencia.tipo_tamizaje.descripcion,
						'observaciones':referencia.observaciones,
					})

				return JsonResponse(lista_resultado_busqueda,safe=False)
				
			else:
				return JsonResponse(lista_resultado_busqueda,safe=False)
	except Exception, e:
		return render(request,'registro/error.html',{'error':e.message})


@login_required
def busqueda_js_contrareferencia(request):
	try:
		if request.method=='GET':
			lista_resultado_busqueda = []
			query_strings=request.GET.keys()
			if query_strings:
				predicados=[]

				fecha_inicial=request.GET['fecha_ini']
				fecha_final=request.GET['fecha_fin']

				if fecha_inicial and fecha_final:
					fecha_inicial=datetime.datetime.strptime(fecha_inicial,'%d/%m/%Y')
					fecha_final=datetime.datetime.strptime(fecha_final,'%d/%m/%Y').replace(hour=23,minute=59)
					predicados.append(('fecha_envio__range',(fecha_inicial,fecha_final)))
				else:
					fecha_inicial=datetime.datetime.strptime('01/01/2000','%d/%m/%Y')
					fecha_final=timezone.now().replace(hour=23,minute=59)
					predicados.append(('fecha_envio__range',(fecha_inicial,fecha_final)))

				if 'unidad_contrarefiere' in request.GET:
					unidad_contrarefiere=request.GET['unidad_contrarefiere']
					if unidad_contrarefiere:
						predicados.append(('unidad_contrarefiere__id',unidad_contrarefiere))

				if 'unidad_recibe' in request.GET:
					unidad_recibe=request.GET['unidad_recibe']
					if unidad_recibe:
						predicados.append(('unidad_recibe__id',unidad_recibe))


				q_list = [Q(x) for x in predicados]
				contrareferencias=Contrareferencia.objects.filter(reduce(operator.and_, q_list))

				
				for contrareferencia in contrareferencias:
					lista_resultado_busqueda.append({
						'fecha_envio':contrareferencia.fecha_envio,
						'unidad_contrarefiere':contrareferencia.unidad_contrarefiere.descripcion,
						'unidad_recibe':contrareferencia.unidad_recibe.descripcion,
						'url':reverse('contrareferencias_paciente',kwargs={'paciente_pk':contrareferencia.paciente.id}),
						'observaciones':contrareferencia.observaciones,
					})

				return JsonResponse(lista_resultado_busqueda,safe=False)
				
			else:
				return JsonResponse(lista_resultado_busqueda,safe=False)
	except Exception, e:
		return render(request,'registro/error.html',{'error':e.message})			


@login_required
def borra_tamizaje(request, elemento_id):
	tamizaje=get_object_or_404(Tamizaje,pk=elemento_id)
	if request.method=='POST':
		try:
			tamizaje.status='C'
			tamizaje.save()
			return JsonResponse({'status':'1','msg' : 'success'},safe=False)			
		except Exception, e:
			return JsonResponse({'status':'0','msg' : e.message},safe=False)			

	return JsonResponse({'status':'0','msg' : 'BAD REQUEST'},safe=False)	

@login_required
def borra_referencia(request, elemento_id):
	referencia=get_object_or_404(Referencia,pk=elemento_id)
	if request.method=='POST':
		try:
			referencia.status='C'
			referencia.save()
			return JsonResponse({'status':'1','msg' : 'success'},safe=False)			
		except Exception, e:
			return JsonResponse({'status':'0','msg' : e.message},safe=False)			

	return JsonResponse({'status':'0','msg' : 'BAD REQUEST'},safe=False)	

@login_required
def borra_contrareferencia(request, elemento_id):
	contrareferencia=get_object_or_404(Contrareferencia,pk=elemento_id)
	if request.method=='POST':
		try:
			contrareferencia.status='C'
			contrareferencia.save()
			return JsonResponse({'status':'1','msg' : 'success'},safe=False)			
		except Exception, e:
			return JsonResponse({'status':'0','msg' : e.message},safe=False)			

	return JsonResponse({'status':'0','msg' : 'BAD REQUEST'},safe=False)			

