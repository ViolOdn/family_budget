from django.urls import include, path
from new_django_project.views import myfunc
from new_django_project.views import main_page
from new_django_project.views import show_login_form, check_name
from new_django_project.views import login_user, do_logout, show_registration_form, register, homework, ajax_path
from django.contrib import admin
from new_django_project.views import show_categories, add_type, add_new_flow_of_funds, show_plan_form
from new_django_project.views import user_plan_settings


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
    path('user_plan_settings', user_plan_settings)
]