from django import template

register = template.Library()

@register.filter(name='update_exec')
def update_exec(exec,value):
	exec = value
	return exec


