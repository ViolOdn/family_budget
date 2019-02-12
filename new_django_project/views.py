from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from new_django_project.models import Categories, FlowOfFunds, ExpensesPlan
import re
from django.http import JsonResponse
import requests
from datetime import datetime, timedelta
import random
from django.utils.translation import ugettext as _
from pymemcache import Client
import pickle

def myfunc(request):
    s = ''
    for x in User.objects.all():
        s = s + x.family_name + ' '

    return HttpResponse(s)


def main_page(request):
    incomes = {}
    incomes = FlowOfFunds.objects.filter(is_it_expense=False)
    expenses = FlowOfFunds.objects.filter(is_it_expense=True)
    sum = 0
    for inc in incomes:
        sum = sum + inc.sum
    for exp in expenses:
        sum = sum - exp.sum

    if request.user.is_authenticated:
        #all_user_flows = {'flows': FlowOfFunds.objects.filter(family_id=request.user)}
        '''
        записать новый словарь с нужными полями из расходов, потом его по значению передать на главную в таблицу
        '''
        return render_to_response('index.html', {'name': request.user.username, 'flag': True,\
                                                 'flows': FlowOfFunds.objects.filter(family_id=request.user),\
                                                 'money': sum})
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
    user = User.objects.create_user(
        request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email']
    )
    return HttpResponseRedirect('/login_form')


def ajax_path(request):
    response = {
    'message': request.POST['a']
    }
    return JsonResponse(response)


def check_name(request):
    ls = []
    for n in User.objects.all():
       ls.append(n.username)
    s = request.POST['name']
    if s in ls:
        response = 1
    else:
        response = 0
    return JsonResponse({'flag':response})


def show_categories(request):
    cat = {'categories': Categories.objects.filter(family_id=request.user)}
    return render_to_response('add_new_type.html', cat)


def add_type(request):
    categories = Categories(family_id=request.user, type_name=request.POST['expense_type'])
    categories.save()
    return HttpResponseRedirect('/')

'''
def get_rates_7_days(request):
    finish_period = datetime.today()
    start_period = finish_period - timedelta(days = 7)
    response = requests.get('http://www.nbrb.by/API/ExRates/Rates/Dynamics/{150}?StartDate=' + start_period + '&' + finish_period)
'''

'''
Для индекс.хтмл:
            <select name="select" size="1">
            {%for category in categories%}
                <option selected value="s"> {{category.type_name}}</option>
              {% endfor %}
            </select>
            Из первостепенного:
            добавление расходов/доходов +
            преобразование дат в соответствующий формат +
            пересчет остатка +
            отображение таблиц
            пересчет планов
            Настройки:
            - накопления
            - день зп
            - 
'''


def add_new_flow_of_funds(request):
    if request.POST['expense_or_income'] == '-':
        exp_type = True
    else:
        exp_type = False
    s = Categories.objects.filter(family_id=request.user)
    type = s.filter(type_name=request.POST['flow_type_choise'])
    old_sum = request.POST['flow_sum']
    if ',' in request.POST['flow_sum']:
        float_sum = old_sum.replace(',', '.')
    else:
        float_sum = request.POST['flow_sum']
    flow_of_funds = FlowOfFunds(family_id=request.user, sum=float_sum, \
                              type_id=type.first(), description=request.POST['flow_description'], \
                                date=request.POST['flow_date'], is_it_expense=exp_type)
    flow_of_funds.save()
    return HttpResponseRedirect('/')
    #return HttpResponse('Расход/доход добавлен. Нажмите кнопку "назад" или Backspace, чтобы вернуться на главную страницу')


def cash_test(request):
    start = datetime.now()
    client = Client(('localhost', 11211))
    expenses = client.get('expenses')
    if expenses is None:
        expenses = []
        i = 1
        while i < 30000:
            s = FlowOfFunds.objects.filter(family_id=random.randint(1, 4)).first()
            expenses.append(s)
            i = i+1
        client.set(
            'expenses',
            pickle.dumps(expenses),
            expire=60
        )
    else:
        expenses = pickle.loads(expenses)
    finish = datetime.now()
    delta = (finish-start).total_seconds()
    return HttpResponse(str(delta))


def no_cash(request):
    start = datetime.now()
    expenses = []
    i = 1
    types = []
    time = ''
    while i < 30000:
        s = FlowOfFunds.objects.filter(family_id=random.randint(1, 4)).first()
        expenses.append(s)
        i = i+1
    delta = (datetime.now()-start).total_seconds()
    time = str(delta) + ' seconds'
    #ttgf
    return HttpResponse(time)


def hello(request):
    return HttpResponse('hello world!')