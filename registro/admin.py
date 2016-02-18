from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Paciente, Tamizaje
from .models import Referencia, Contrareferencia
from .models import Tipo_Unidad, Unidad, Tipo_Tamizaje, Tipo_Tratamiento
from .models import Estado, Municipio, Localidad
from .models import Usuario_Unidad, Usuario_Perfil
from .models import Resultado,Unidad_Asignacion




#inlines
class Usuario_Perfil_Inline(admin.StackedInline):
    model = Usuario_Perfil
    can_delete = False
    verbose_name_plural = 'Perfil de usuario'

class Usuario_Unidad_Inline(admin.StackedInline):
	model = Usuario_Unidad
	can_delete = False
	verbose_name_plural = 'Unidades de usuario'	

class ReferenciaInline(admin.StackedInline):
	model = Referencia




#admin models

class PacienteAdmin(admin.ModelAdmin):
	inlines = [ReferenciaInline]

class UserAdmin(UserAdmin):
	list_display=['username','first_name','last_name','email','is_staff','last_login','is_active']
	ordering = ('-last_login',)
	inlines = [Usuario_Perfil_Inline, Usuario_Unidad_Inline]





admin.site.register(Paciente, PacienteAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tipo_Unidad) 
admin.site.register(Unidad) 
admin.site.register(Tipo_Tamizaje)
admin.site.register(Tipo_Tratamiento)
admin.site.register(Resultado)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Localidad)
admin.site.register(Unidad_Asignacion)