from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from new_django_project.models import Categories, FlowOfFunds, ExpensesPlan, SavingMoney
import re
from django.http import JsonResponse
import requests
from datetime import datetime, timedelta
import random
from django.utils.translation import ugettext as _
from pymemcache import Client
import pickle
#from new_django_project.models import Human

def myfunc(request):
    s = ''
    for x in User.objects.all():
        s = s + x.family_name + ' '

    return HttpResponse(s)


def main_page(request):
    if request.user.is_authenticated:
        incomes = {}
        incomes = FlowOfFunds.objects.filter(family_id=request.user)
        sum = 0
        for inc in incomes:
            sum = sum + inc.sum
        '''
        записать новый словарь с нужными полями из расходов, потом его по значению передать на главную в таблицу
        '''
        if SavingMoney.objects.filter(user_id=request.user):
            today = str(datetime.today())
            year = int(today[0:4])
            month = int(today[5:7])
            day = int(today[8:10])
            sal_day = int(SavingMoney.objects.filter(user_id=request.user).first().salary_day)
            start_salary_date = datetime(year, month, sal_day)
            today_date = datetime(year, month, day)
            if sal_day < day:
                if month < 12:
                    finish_salary_date = datetime(year, month + 1, sal_day)
                else:
                    finish_salary_date = datetime(year + 1, 1, sal_day)
            else:
                n = sal_day - day
                finish_salary_date = today_date + timedelta(days = n)
            delta = (finish_salary_date - today_date).days

            plans = ExpensesPlan.objects.filter(user_id=request.user)
            types = Categories.objects.filter(family_id=request.user, is_it_expense=True)
            i = 0
            names = []
            while i < len(types):
                names.append(types.filter(type_name=types[i].type_name).first().type_name)
                i = i+1
            all_plan_sum = []
            all_money_spent = []
            rest_of_money = []
            n = 0

            while n < len(plans):
                plan = plans[n]
                all_plan_sum.append(plan.sum_plan)
                money_spent = FlowOfFunds.objects.filter(family_id=request.user)
                money_spent = money_spent.filter(type_id=plan.type_id) #что блять сука не так какого хера пустое множество
                mon_sum = 0
                for mon in money_spent:
                    mon_sum = mon_sum + mon.sum
                all_money_spent.append(abs(mon_sum))
                rest_of_money.append(plan.sum_plan-abs(mon_sum))
                n = n+1
            final_list = []
            fl = []
            i = 0
            while i < len(names):
                fl = []
                fl.append(names[i])
                fl.append(all_plan_sum[i])
                fl.append(all_money_spent[i])
                fl.append(rest_of_money[i])
                final_list.append(fl)
                i = i+1
            days = SavingMoney.objects.filter(user_id=request.user).first().salary_day


            return render_to_response('index.html', {'name': request.user.username, 'flag': True,\
                                                 'flows': FlowOfFunds.objects.filter(family_id=request.user),\
                                                 'money': sum, 'delta': delta, 'plans': final_list, \
                                                     'sum_euro': SavingMoney.objects.filter(user_id=request.user).first().euro, \
                                                     'sum_dollars': SavingMoney.objects.filter(user_id=request.user).first().dollars})
        else:
            return render_to_response('index.html', {'name': request.user.username, 'flag': True, \
                                                     'flows': FlowOfFunds.objects.filter(family_id=request.user), \
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
    if request.POST['expense_or_income'] == '-':
        exp_type = True
    else:
        exp_type = False
    categories = Categories(family_id=request.user, type_name=request.POST['expense_type'], is_it_expense=exp_type)
    categories.save()
    return HttpResponseRedirect('/')


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
            отображение таблиц +
            пересчет планов +
            Настройки: +
            - накопления
            - день зп
            
'''


def add_new_flow_of_funds(request):
    s = Categories.objects.filter(family_id=request.user)
    type = s.filter(type_name=request.POST['flow_type_choise'])
    old_sum = request.POST['flow_sum']
    if ',' in request.POST['flow_sum']:
        float_sum = old_sum.replace(',', '.')
    else:
        float_sum = request.POST['flow_sum']
    float_sum = float(float_sum)
    if type.first().is_it_expense:
        float_sum = float_sum * (-1)
    flow_of_funds = FlowOfFunds(family_id=request.user, sum=float_sum, \
                              type_id=type.first(), description=request.POST['flow_description'], \
                                date=request.POST['flow_date'])
    flow_of_funds.save()
    return HttpResponseRedirect('/')


def show_plan_form(request):
    s = Categories.objects.filter(family_id=request.user, is_it_expense=True)
    plan = {'categories': s}
    return render_to_response('user_settings.html', plan)


def user_plan_settings(request):
    types = Categories.objects.filter(family_id=request.user, is_it_expense=True)
    n = len(types)
    i = 0

    today = str(datetime.today())
    year = int(today[0:4])
    month = int(today[5:7])
    day = int(today[9:11])
    sal_day = int(SavingMoney.objects.filter(user_id=request.user).first().salary_day)
    start_salary_date = datetime(year, month, sal_day)
    today_date = datetime(year, month, day)
    if sal_day > day:
        if month < 12:
            finish_salary_date = datetime(year, month + 1, sal_day)
        else:
            finish_salary_date = datetime(year + 1, 1, sal_day)
    else:
        finish_salary_date = today_date + (sal_day - day)
    delta = (finish_salary_date - today_date).days

    SavingMoney.objects.filter(user_id=request.user).delete()
    saving_money = SavingMoney(user_id=request.user, euro=request.POST['sum_euro'], \
                               dollars=request.POST['sum_dollars'], salary_day=request.POST['salary_date'])
    saving_money.save()

    ExpensesPlan.objects.filter(user_id=request.user).delete()
    while i < n:
        current_type_id = types.filter(type_name=types[i].type_name).first().type_id
        new_id = Categories.objects.filter(family_id=request.user, is_it_expense=True, type_name=types[i].type_name).first().type_id
        field_name = types.filter(type_name=types[i].type_name).first().type_name
        old_sum = request.POST[field_name]
        if ',' in request.POST[field_name]:
            float_sum = old_sum.replace(',', '.')
        else:
            float_sum = request.POST[field_name]
        #ExpensesPlan.objects.filter(user_id=request.user).delete()
        expenses_plan = ExpensesPlan(user_id=request.user, type_id=types.filter(type_name=types[i].type_name).first(), sum_plan=float_sum, start_date=start_salary_date, finish_date=finish_salary_date)
        expenses_plan.save()
        i = i+1

    return HttpResponseRedirect('/''')
    #return HttpResponse('ok')
