from django.template.defaulttags import register
from django.core.urlresolvers import resolve
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import F
from django.conf import settings
import uuid
import base64
import re
import datetime
from datetime import date
import os
import random
import string
import ntpath

@register.filter(name='file_name')
def nomeArquivo(caminho):
    return ntpath.basename(caminho)

@register.filter(name='file_exists')
def file_exists(filepath, filename=None):
    if filepath == None:
        return None
    if filename != None:
        file = os.path.join(filepath, filename)
    else:
        file = filepath
    if os.path.isfile(file):
        return file
    else:
        return None

@register.filter(name='ramdom_color')
def ramdom_color(x):
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

@register.filter(name='base64crypt')
def base64crypt(message):
    enc = base64.b64encode(message.encode('utf-8'))
    return enc

@register.filter
def parse_date(date_string, format):
    """
    Return a datetime corresponding to date_string, parsed according to format.
    For example, to re-display a date string in another format::
        {{ "01/01/1970"|parse_date:"%m/%d/%Y"|date:"F jS, Y" }}
    """
    try:
        return datetime.datetime.strptime(date_string, format)
    except ValueError:
        return None

@register.filter
def viewname(req):
    res = resolve(req.path_info)
    return res.namespace+':'+res.url_name

@register.filter
def urlname(req):
    res = resolve(req.path_info)
    return res.url_name

@register.filter
def has_perm(perm, user):
    return user.has_perm(perm)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def indexOf(list, work):
    return list.index(work)


def checkPaswStrength(password, tamanho=8):
    if password==None or password=='':
        return "A senha não pode estar em branco"
    if not re.search(r'\d', password):
        return "A senha deve conter ao menos um digito numérico"
    if not re.search(r'[A-Z]', password):
        return "A senha deve conter ao menos uma letra em maiúculo"
    if not re.search(r'[a-z]', password):
        return "A senha deve conter ao menos uma letra em minúculo"
    if len(password) < tamanho:
        return "Tamanho mínimo da senha é %s" % str(tamanho)
    return True


def handle_uploaded_file(f):
    filename = str(uuid.uuid4())+".pfx"
    with open(join(settings.MEDIA_ROOT, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


def padString(source):
    paddingChar = ' '
    size = 16
    padLength = size - len(source) % size;
    for i in range(0, padLength):
        source += paddingChar
    return source


#def randomPass(size=settings.TAMANHO_SENHA_EMAIL):
#    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def first_day_of_month(d):
    return date(d.year, d.month, 1)
