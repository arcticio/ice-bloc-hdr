

from django.template import Library
from django.utils.text import truncate_html_words
from django.template.defaultfilters import wordcount
## http://code.djangoproject.com/svn/django/trunk/django/template/defaultfilters.py

from config import BLOG

register = Library()

## http://djangosnippets.org/snippets/1595/
def feedparsed(value):
    return datetime.datetime(*value[:6])
register.filter(feedparsed)


def favicon(link):
  import urlparse
  scheme, domain, path, params, query, fragment = urlparse.urlparse(link)
  return scheme + "://" + domain + "/favicon.ico"
register.filter(favicon)


## http://cmyk.sevennineteen.com/blogs/code/controlling-post-truncation-django/

#@register.filter('clear_trunc')
def needs_trunc(value, max_words):
  if BLOG['truncater'] in value:
    return True
  if wordcount(value) > max_words :
    return True
  return False

register.filter(needs_trunc)


#@register.filter('control_trunc')
def control_trunc(value, max_words):
  if BLOG['truncater'] in value:
    return value[:value.find(BLOG['truncater'])]
  if wordcount(value) > max_words :
    return truncate_html_words(value, max_words)
  else:
    return value

register.filter(control_trunc)

#@register.filter('clear_trunc')
def clear_trunc(value):
  return value.replace(BLOG['truncater'], '')
register.filter(clear_trunc)



