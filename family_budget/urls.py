from django.urls import include, path
from family_budget.views import *
from django.contrib import admin

urlpatterns = [
    path('mypath', myfunc),
    path('', main_page),
    path('login_form', show_login_form),
    path('login', login_user),
    path('success_logout', do_logout),
    path('registration_form', show_registration_form),
    path('register', register),
    path('homework', homework),
    path('ajax_path', ajax_path),
    path('check_name', check_name),
    path('admin/', admin.site.urls),
    path('show_categories', show_categories),
    path('add_type', add_type),
    path('add_new_flow_of_funds', add_new_flow_of_funds),
    path('user_settings', show_plan_form),
    path('user_plan_settings', user_plan_settings),
    path('show_details_form', show_details_form),
    path('get_details_info', get_details_info),
    path('add_new_part', add_new_part)
]