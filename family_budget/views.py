import datetime
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from family_budget.models import Categories, FlowOfFunds, ExpensesPlan, SavingMoney
from django.http import JsonResponse
from datetime import datetime, timedelta
import csv

def main_page(request):
    if request.user.is_authenticated:
        incomes = FlowOfFunds.objects.filter(family_id=request.user)
        sum = 0
       # sum = FlowOfFunds.objects.filter(family_id=request.user).aggregate(Sum('sum')) - как это работает?
        for inc in incomes:
            sum = sum + inc.sum
        if SavingMoney.objects.filter(user_id=request.user):
            today = datetime.today()
            '''
            year = int(today[0:4])
            month = int(today[5:7])
            day = int(today[8:10])
            '''
            sal_day = SavingMoney.objects.filter(user_id=request.user).first().salary_day
            # start_salary_date = datetime(year, month, sal_day)
            today_date = datetime.fromordinal(today.toordinal())
            if sal_day < today().day:
                if today().month < 12:
                    finish_salary_date = datetime(today().year, today().month + 1, sal_day)
                else:
                    finish_salary_date = datetime(today().year + 1, 1, sal_day)
            else:
                n = sal_day - today().day
                finish_salary_date = today_date + timedelta(days=n)
            delta = (finish_salary_date - today_date).days

            plans = ExpensesPlan.objects.filter(user_id=request.user)
            types = Categories.objects.filter(family_id=request.user, is_it_expense=True)
            i = 0
            '''
            names = []
            while i < len(types):
                names.append(types.filter(type_name=types[i].type_name).first().type_name)
                i = i+1
            '''
            names = [type.type_name for type in types]
            all_plan_sum = []
            all_money_spent = []
            rest_of_money = []
            n = 0

            for plan in plans:
                all_plan_sum.append(plan.sum_plan)
                money_spent = FlowOfFunds.objects.filter(family_id=request.user, type_id=plan.type_id)
                mon_sum = 0
                for mon in money_spent:
                    mon_sum = mon_sum + mon.sum
                all_money_spent.append(abs(mon_sum))
                rest_of_money.append(plan.sum_plan-abs(mon_sum))
            final_list = []
            fl = []
            i = 0
            for name in names:
                fl = []
                fl.append(name)
                fl.append(all_plan_sum[i])
                fl.append(all_money_spent[i])
                fl.append(rest_of_money[i])
                final_list.append(fl)
                i = i+1
           # days = SavingMoney.objects.filter(user_id=request.user).first().salary_day


            return render_to_response('index.html', {
                'name': request.user.username, 'flag': True,\
                'flows': FlowOfFunds.objects.filter(family_id=request.user).order_by('date'),\
                'money': sum, 'delta': delta, 'plans': final_list,\
                'sum_euro': SavingMoney.objects.filter(user_id=request.user).first().euro,\
                'sum_dollars': SavingMoney.objects.filter(user_id=request.user).first().dollars,\
                'categories': Categories.objects.filter(family_id=request.user)}
                                      )
        else:
            return render_to_response('index.html', {
                'name': request.user.username, 'flag': True,\
                'flows': FlowOfFunds.objects.filter(family_id=request.user),\
                'money': sum,\
                'categories': Categories.objects.filter(family_id=request.user)}
                                      )

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
    return render_to_response('add_new_part_of_plan.html', {'new_type': Categories.objects.filter(is_it_expense=True).last().type_name})

'''
def show_new_part_form(request):
    return render_to_response('add_new_part_of_plan.html.html')
    '''


def add_new_flow_of_funds(request):
    s = Categories.objects.filter(family_id=request.user)
    type = s.filter(type_name=request.POST['choise_of_expenses'])
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
    sal_day = int(request.POST['salary_date'])
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


def show_details_form(request):
    return render_to_response("details_form.html")


def get_details_info(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = "Flow of Funds Info.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response, csv.excel)
    writer.writerow(['Сумма руб', 'Тип', 'Описание', 'Дата'])
    x = '22/11/1963'
    new_x = datetime.strptime(x, '%d/%m/%Y').date()
    flow_of_fund = FlowOfFunds.objects.filter \
        (date__gte=datetime.strptime(request.POST['start_date'], '%Y-%m-%d'), \
         date__lte=datetime.strptime(request.POST['finish_date'], '%Y-%m-%d'))
    for flow in flow_of_fund:
        writer.writerow([flow.sum, flow.type_id.type_name, flow.description, flow.date])
    return response


def add_new_part(request):
    current_type_id = Categories.objects.filter(is_it_expense=True).last()
    field_name = Categories.objects.filter(is_it_expense=True).last().type_name
    old_sum = request.POST['new_type_name']
    if ',' in request.POST['new_type_name']:
        float_sum = old_sum.replace(',', '.')
    else:
        float_sum = request.POST['new_type_name']
        #ExpensesPlan.objects.filter(user_id=request.user).delete()
    expenses_plan = ExpensesPlan(user_id=request.user, type_id=current_type_id, sum_plan=request.POST['new_type_name'], start_date=ExpensesPlan.objects.first().start_date, finish_date=ExpensesPlan.objects.first().finish_date)
    expenses_plan.save()
    #return HttpResponse('ok')
    return HttpResponseRedirect('/''')



#excelt библиотека скачать