from django import template

register = template.Library()

def get_key(dict,key):
    return dict.get(key)

register.filter('get_key',get_key)

def get_index(list,index):
    return list[index]

register.filter('get_index',get_index)
