from django.shortcuts import render
from django.http import HttpResponse
import datetime
from new_django_project.models import Family
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from new_django_project.models import Family
import re


def myfunc(request):
    s = ''
    for x in Family.objects.all():
        s = s + x.family_name + ' '

    return HttpResponse(s)


def main_page(request):
    if request.user.is_authenticated:
        return render_to_response('index.html', {'name': request.user.username, 'flag': True})
    else:
        return render_to_response('index.html', {'flag': False})


def homework(request):
    return render_to_response('homework.html')


def login_user(request):
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is None:
        return render_to_response('error.html',{})
    else:
        login(request, user)
        return HttpResponseRedirect('/')


def show_login_form(request):
    return render_to_response('login.html', {})


def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Вы не залогинены')


def show_registration_form(request):
    return render_to_response('register.html', {})


def register(request):
    while True:
        if '@' in request.POST['email']:
            break
        else:
            return HttpResponse('Введите корректный e-mail')
    user = User.objects.create_user(
        request.POST['username'],
        password=request.POST['password']
    )

    family = Family(family_name=user, family_email=request.POST['email'], password_hash='123')
    family.save()
    return HttpResponseRedirect('/login_form')
