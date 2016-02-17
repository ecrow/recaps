#encoding:utf-8
from django import template
import datetime


register = template.Library()

@register.filter('fpp')
def calcula_fpp(fum):
	''' Calcula la fecha probable de parto con base en la fum '''
	try:
		 
		return fum + datetime.timedelta(days=277)
		
	except Exception, e:
		return None


@register.filter('sg')
def calcula_fpp(fum):
	''' Calcula las semanas de gestación con base en la fum '''
	try:
		semanas = (datetime.datetime.now() - fum).days / 7
		dias = (datetime.datetime.now() - fum).days % 7
		return str(semanas)+'.'+str(dias) 

	except Exception, e:
		return None

