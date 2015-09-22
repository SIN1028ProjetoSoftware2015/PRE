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


def paginar(kwargs, model, ordem_default, context, listFields, maximo_paginas = 5, lista_fetch=None, order_type='desc'):
    """
    Método de paginação padrão para todas as tabelas da aplicação, recebe os seguintes parâmetros
    :param kwargs: ponteiro de parametros que contém a pagina, ordem, tipo de ordem, quentidade por pagina e filtros para a busca
    :param model: classe dos objetos que seráo buscados
    :param ordem_default: atributo de ordenção default para paginação
    :param context: objeto contexto da requisição, este será retornado com a lista de atributos da paginação no final do método
    :param listFields: lista de atributos da classe em questão
    :param maximo_paginas: quantidade maxima de botões que representarão as paginas
    :return: o objeto de contexto
    """
    if lista_fetch == None:
        lista_fetch = []
    page = 1
    if 'page' in kwargs:
        try:
            page = int(kwargs['page'])
        except:
            pass
    order = ordem_default
    idxOrder = listFields.index(order)
    if 'order' in kwargs:
        try:
            idxOrder = int(kwargs['order'])
            order = listFields[ idxOrder ]
        except:
            pass
    tpOrder = order_type
    if 'tpOrder' in kwargs:
        try:
            tpOrder = kwargs['tpOrder']
        except:
            pass
    paginate_by = 50
    if 'qtdPage' in kwargs:
        try:
            paginate_by = int(kwargs['qtdPage'])
        except:
            pass

    context['page'] = page
    context['idxorder'] = idxOrder
    context['order'] = order
    context['fields'] = listFields
    context['tpOrder'] = tpOrder
    if tpOrder == 'asc':
        context['tpOrderInv'] = 'desc'
    else:
        context['tpOrderInv'] = 'asc'

    list_docs = []
    last_page = 1
    if page < 1:
        page = 1
    params = {}
    if 'params' in kwargs:
        params = kwargs['params']
    total = model.objects.filter(**params).count()
    if total > 0:
        last_page = int(total/paginate_by)
        if total % paginate_by > 0:
            last_page += 1
        if page > last_page:
            page = last_page
        if order != None:
            if tpOrder == 'desc':
                order = '-'+order
            list_docs = model.objects.filter(**params).prefetch_related(*lista_fetch).order_by(order)[(page-1)*paginate_by: (page-1)*paginate_by+paginate_by]
        else:
            list_docs = model.objects.filter(**params)[(page-1)*paginate_by: (page-1)*paginate_by+paginate_by]
    context['object_list'] = list_docs
    listacontrol = []
    left = int(maximo_paginas/2)+1 #mais um para que nao contabilize a propria pagina
    idxL = page
    while left > 0 and idxL > 0:
        listacontrol.append(idxL)
        idxL -= 1
        left -= 1
    right = int(maximo_paginas/2) + left
    idxR = page+1
    while right > 0 and idxR < last_page+1:
        listacontrol.append(idxR)
        idxR += 1
        right -= 1
    if right > 0: #se sobrou espaco pra direita
        left = right
        while left > 0 and idxL > 0:
            listacontrol.append(idxL)
            idxL -= 1
            left -= 1
    context['object_range'] = sorted(set(listacontrol))
    context['object_page'] = page
    context['object_count'] = total
    context['object_last'] = last_page
    context['object_previous'] = page-1
    context['object_next'] = page+1
    context['object_qtdpage'] = paginate_by
    return context

