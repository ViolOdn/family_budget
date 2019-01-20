from django.urls import include, path
from new_django_project.views import myfunc
from new_django_project.views import main_page
from new_django_project.views import show_login_form
from new_django_project.views import login_user, do_logout, show_registration_form, register, homework


urlpatterns = [
    path('mypath', myfunc),
    path('', main_page),
    path('login_form', show_login_form),
    path('login', login_user),
    path('success_logout', do_logout),
    path('registration_form', show_registration_form),
    path('register', register),
    path('homework', homework)

]