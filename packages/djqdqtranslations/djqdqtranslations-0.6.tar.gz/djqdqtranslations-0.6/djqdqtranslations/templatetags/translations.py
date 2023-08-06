from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='span_wrap')
@stringfilter
def span_wrap(text, text_class=""):
    return mark_safe(u"<span class='{}'>{}</span>".format(text_class,text))
