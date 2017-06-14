from django.template import Library


register = Library()

@register.filter
def format_url(url):
    """format url add a scheme:http or https"""
    if url:
        scheme = "http"
        a = url if scheme in url else scheme + "://" + url
        return url if scheme in url else scheme + "://" + url