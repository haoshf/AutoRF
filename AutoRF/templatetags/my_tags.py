from django import template
from django.utils.safestring import mark_safe

register = template.Library()
@register.filter(name = 'add_str')
def add_str(reg,reg2):
  return '{0}-{1}'.format(str(reg),str(reg2))