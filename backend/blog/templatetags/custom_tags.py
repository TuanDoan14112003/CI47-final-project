from django.template.defaulttags import register
@register.filter
def get_item(dict,key):
    return dict.get(key)