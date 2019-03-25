# -*- coding: utf-8 -*-


import json
import logging


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.shortcuts import render
from django.views.generic import TemplateView


from utils.generics import get_date_from_timezone


logger = logging.getLogger(__name__)


class LoginRequiredMixin(object):

    @classmethod
    def as_view(self, **kwargs):
        # type: (object) -> object
        view = super(LoginRequiredMixin, self).as_view(**kwargs)
        return login_required(view, login_url='/login/')


class ProfileTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        """ Root del template del perfil
        """
        return render(request, 'autenticacion/profile.html')

    def post(self, request, *args, **kwargs):
        """ Método para cambiar la contraseña del usuario
        """
        try:
            body = QueryDict(request.body)
            user = User.objects.get(pk=request.user.id)
            new_password1 = body.get('new_password1')
            new_password2 = body.get('new_password2')
            if user.date_joined is None:
                user.date_joined = get_date_from_timezone()
                user.save()
            if user.last_login is None:
                user.last_login = get_date_from_timezone()
                user.save()
            if new_password1 and new_password2 is not None:
                user.set_password(new_password1)
                user.save()
                return HttpResponse(json.dumps('Contraseña cambiada exitosamente, por favor inicie sesión nuevamente.'),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps('No se pudo cambiar la contraseña.'),
                                    content_type='application/json')
        except Exception, e:
            logger.error(e)
            return HttpResponse(e)

    def patch(self, request, *args, **kwargs):
        """ Método para cambiar datos del usuario
        """
        try:
            body = QueryDict(request.body)
            user = User.objects.get(pk=request.user.id)
            first_name = body.get('first_name')
            last_name = body.get('last_name')
            if user.date_joined is None:
                user.date_joined = get_date_from_timezone()
                user.save()
            if user.last_login is None:
                user.last_login = get_date_from_timezone()
                user.save()
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return HttpResponse(json.dumps('Registro actualizado exitosamente.'),
                                content_type='application/json')
        except Exception, e:
            logger.error(e)
            return HttpResponse(e)


def home_to_dashboard(request):
    return HttpResponseRedirect(reverse('dashboard:index'))


def log_in(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse('dashboard:index'))
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    try:
                        next = request.GET['next']
                        return HttpResponseRedirect(next)
                    except:
                        return HttpResponseRedirect(reverse('dashboard:index'))
                else:
                    return HttpResponse("Usuario no activo")
            else:
                return HttpResponseRedirect('/login/')
    else:
        formulario = AuthenticationForm()
    return render(request, 'autenticacion/login.html', {formulario: formulario})


@login_required(login_url='/login/')
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')
