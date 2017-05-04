from django import template
import urllib
register = template.Library()


def print_decoded_uri(uri):
    return urllib.unquote(urllib.unquote(uri))

register.filter(print_decoded_uri)
