from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


status=(('A','Activo'),('C','Cancelado'))


class Resultado(models.Model):
	descripcion = models.CharField(max_length=50)
	status=models.CharField(max_length=1,choices=status,default='A')

	def __str__(self):
		return self.descripcion

class Tipo_Unidad(models.Model):
	descripcion = models.CharField(max_length=50)
	status=models.CharField(max_length=1,choices=status,default='A')

	class Meta:
		verbose_name_plural = 'Tipos de unidades'

	def __str__(self):
		return self.descripcion


class Unidad(models.Model):
	clues = models.CharField(max_length=11)
	descripcion = models.CharField(max_length=300)
	tipo_unidad = models.ForeignKey(Tipo_Unidad)
	status=models.CharField(max_length=1,choices=status,default='A')

	class Meta:
		verbose_name_plural = 'Unidades'

	def __unicode__(self):
		return '{}'.format(self.descripcion)


class Tipo_Tamizaje(models.Model):
	descripcion = models.CharField(max_length=100)
	status=models.CharField(max_length=1,choices=status,default='A')

	class Meta:
		verbose_name_plural = 'Tipo de tamizajes'

	def __unicode__(self):
		return self.descripcion



class Tipo_Tratamiento(models.Model):
	descripcion = models.CharField(max_length=100)
	status=models.CharField(max_length=1,choices=status,default='A')

	class Meta:
		verbose_name_plural = 'Tipo de tratamientos'

	def __unicode__(self):
		return self.descripcion

class Estado(models.Model):
	clave=models.CharField(max_length=2)
	descripcion=models.CharField(max_length=100)
	abreviatura=models.CharField(max_length=50)
	status=models.CharField(max_length=1,choices=status,default='A')

	def __unicode__(self):
		return self.descripcion

class Municipio(models.Model):
	estado=models.ForeignKey(Estado)
	clave=models.CharField(max_length=3)
	descripcion=models.CharField(max_length=150)
	status=models.CharField(max_length=1,choices=status,default='A')

	def __unicode__(self):
		return u'{} - {}'.format(self.clave,self.descripcion)


class Localidad(models.Model):
	municipio = models.ForeignKey(Municipio)
	clave = models.CharField(max_length=4)
	descripcion = models.CharField(max_length=150)
	status=models.CharField(max_length=1,choices=status,default='A')

	class Meta:
		verbose_name_plural = 'Localidades'
	
	def __unicode__(self):
		return u'Municipio: {} - Localidad: {}-{}'.format(self.municipio.clave,self.clave,self.descripcion)

class Paciente(models.Model):
	nombre = models.CharField(max_length=100)
	apellido_paterno = models.CharField(max_length=50)
	apellido_materno = models.CharField(max_length=50)
	edad = models.IntegerField()
	unidad = models.ForeignKey(Unidad)
	usuario_registro = models.ForeignKey(User)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	status=models.CharField(max_length=1,choices=status,default='A')

	def __unicode__(self):
		return '%s %s %s' % (self.nombre,self.apellido_paterno,self.apellido_materno)

class Domicilio(models.Model):
	paciente = models.ForeignKey(Paciente)
	localidad = models.ForeignKey(Localidad)
	domicilio = models.TextField(blank=True)
	telefono=models.CharField(max_length=10,blank=True, null=True)
	usuario_registro = models.ForeignKey(User)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	status=models.CharField(max_length=1,choices=status,default='A')

	def __unicode__(self):
		return u'{}'.format(self.localidad)

	def get_domicilio_completo(self):
		return u'{} {} {} {}'.format(
			self.localidad.municipio.estado.descripcion,
			self.localidad.municipio.descripcion,
			self.localidad.descripcion,
			self.domicilio
		)		

class Obstetrico(models.Model):
	paciente = models.ForeignKey(Paciente)
	fum = models.DateTimeField()
	ultrasonido = models.BooleanField(default=False)
	gesta = models.IntegerField()
	factores_riesgo = models.TextField(blank=True)
	usuario_registro = models.ForeignKey(User)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	status=models.CharField(max_length=1,choices=status,default='A')



class Referencia(models.Model):
	paciente = models.ForeignKey(Paciente)
	tipo_tamizaje = models.ForeignKey(Tipo_Tamizaje)
	unidad_refiere = models.ForeignKey(Unidad, related_name='unidad_refiere')
	unidad_recibe = models.ForeignKey(Unidad)
	fecha_envio = models.DateTimeField(default=timezone.now)
	observaciones = models.TextField(blank=True)
	usuario_registro = models.ForeignKey(User)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	status=models.CharField(max_length=1,choices=status,default='A')
	
	
class Tamizaje(models.Model):
	paciente = models.ForeignKey(Paciente)
	fecha_consulta = models.DateTimeField(default=timezone.now)
	unidad_realiza = models.ForeignKey(Unidad)
	tipo_tamizaje = models.ForeignKey(Tipo_Tamizaje)
	resultado = models.ForeignKey(Resultado)
	tipo_tratamiento = models.ForeignKey(Tipo_Tratamiento)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	usuario_registro = models.ForeignKey(User)
	status=models.CharField(max_length=1,choices=status,default='A')


class Contrareferencia(models.Model):
	paciente = models.ForeignKey(Paciente)
	unidad_contrarefiere = models.ForeignKey(Unidad,related_name='unidad_contrarefiere')
	unidad_recibe = models.ForeignKey(Unidad)
	fecha_envio = models.DateTimeField(default=timezone.now)
	observaciones = models.TextField(blank=True)
	usuario_registro = models.ForeignKey(User)
	fecha_registro = models.DateTimeField(default=timezone.now)
	status=models.CharField(max_length=1,choices=status,default='A')


class Usuario_Unidad(models.Model):
	usuario = models.ForeignKey(User)
	unidad = models.ForeignKey(Unidad)
	status=models.CharField(max_length=1,choices=status,default='A')


class Unidad_Asignacion(models.Model):
	envia = models.ForeignKey(Unidad, related_name='envia')
	recibe = models.ForeignKey(Unidad)
	status=models.CharField(max_length=1,choices=status,default='A')
	class Meta:
		verbose_name_plural = 'Unidad_Asignaciones'

	def __unicode__(self):
		return u'{} -> {}'.format(self.envia.descripcion, self.recibe.descripcion)


class Usuario_Perfil(models.Model):
	usuario=models.OneToOneField(User)
	apellido_materno=models.CharField(max_length=50)



