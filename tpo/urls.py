from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.loginre, name='login'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('details', views.details, name='details'),
    path('company_details', views.cdetails, name='company_details'),
    path('job_details', views.jdetails, name='job_details'),
    path('view_job', views.job, name='view_job'),
    path('apply_job', views.apply, name='apply_job'),
    path('applicant', views.applicant, name='applicant'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('account', views.account, name='account'),
    path('update', views.update, name='update'),
    path('company_update', views.company_update, name='company_update'),
    path('change_password', views.changepassword, name='change_password'),
    path('canceljob', views.canceljob, name='canceljob'),
    path('forgot_password', views.forgot_password, name='forgot_password')
]
