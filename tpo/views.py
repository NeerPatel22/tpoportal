import hashlib
import math
import random

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

# from django.contrib.sessions.models import Session
from .models import login, student_info, company_details, job_details, job_applicant


# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    """ Method for register """
    if request.method == 'POST':
        role = request.POST['role']
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['psw']
        cpassword = request.POST['cpsw']
        email = request.POST['email']

        if password == cpassword:
            uv = login.objects.filter(USERNAME=username)
            if uv.count() > 0:
                messages.error(request, 'Username is Taken')
                return redirect('register')
            else:
                password1 = hashlib.md5(str.encode(password)).hexdigest()
                user = login(NAME=name, USERNAME=username, PASSWORD=password1, EMAILID=email, ROLE=role)
                user.save()
                messages.success(request, 'Register successful')
                return redirect('login')
        else:
            messages.error(request, 'Password and Confirm password Not Match')
            return redirect('register')
    else:
        return render(request, 'signup.html')


def loginre(request):
    """ Method for login """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        password = hashlib.md5(str.encode(password)).hexdigest()

        if login.objects.filter(USERNAME=username, PASSWORD=password).exists():
            log = login.objects.get(USERNAME=username)
            role = log.ROLE
            request.session['username'] = username
            request.session['role'] = role
            return redirect('home')
        else:
            messages.error(request, 'invalid credentials', extra_tags='alert')
            return redirect('login')
    else:
        return render(request, 'login.html')


def home(request):
    """ Method for home page after login"""
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        return render(request, 'home.html', {'role': role, 'username': user})
    return redirect('login')


def logout(request):
    del request.session['username']
    del request.session['role']
    return redirect('/')


def details(request):
    """ Method to add student details """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        if request.method == 'POST':
            uname = request.session['username']
            er = request.POST['er']
            fn = request.POST['fname']
            mn = request.POST['mname']
            ln = request.POST['lname']
            mnum = request.POST['mnum']
            email = request.POST['eid']
            sem = request.POST['sem']
            bran = request.POST['bran']
            addy = request.POST['add']
            poy = request.POST['poy']
            dob = request.POST['dob']
            bg = request.POST['bg']
            gen = request.POST['g']
            grad = request.POST['grade']
            resume = request.FILES['resume']

            uc = student_info.objects.filter(USERNAME=uname)
            if uc.count() > 0:
                messages.error(request, 'You had already added your details')
                return redirect('details')
            else:
                details = student_info(Enrollment=er, USERNAME=uname, FirstName=fn, MiddleName=mn, LastName=ln,
                                       MobileNo=mnum, email=email, Semester=sem, Branch=bran, AdmissionYear=addy,
                                       PassOutYear=poy, DOB=dob, BloodGroup=bg, Gender=gen, OverallGrade=grad,
                                       Resume=resume)
                details.save()
                messages.success(request, 'Details Add successfully')
                return redirect('details')
        else:
            return render(request, 'student_details.html', {'role': role, 'username': user})
    else:
        return redirect('login')


def cdetails(request):
    """ Method to add company details """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        if request.method == 'POST':
            uname = request.session['username']
            cname = request.POST['cname']
            hrname = request.POST['hrname']
            email = request.POST['email']
            add = request.POST['add']
            link = request.POST['wl']

            un = company_details.objects.filter(USERNAME='uname')
            if un.count() > 0:
                messages.error(request, 'You had already added your details')
                return redirect('company_details')
            else:
                cds = company_details(COMPANYNAME=cname, USERNAME=uname, HRNAME=hrname, EMAILID=email, ADDRESS=add,
                                      WEBLINK=link)
                cds.save()
                messages.success(request, 'Details Add successfully')
                return redirect('company_details')
        else:
            return render(request, 'company_details.html', {'role': role, 'username': user})
    else:
        return redirect('login')


def jdetails(request):
    """ Method to add job """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        if request.method == 'POST':
            cname = request.POST['cname']
            des = request.POST['des']
            ec = request.POST['ec']
            jd = request.POST['jd']

            jobd = job_details(COMPANYNAME=cname, DESIGNATION=des, ELIGIBILITYCRITERIA=ec, JOBDESCRIPTION=jd)
            jobd.save()
            messages.success(request, 'Job Details Add successfully')
            return redirect('job_details')
        else:
            return render(request, 'job_details.html', {'role': role, 'username': user})
    else:
        return redirect('login')


def job(request):
    """ Method for display job """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        job = job_details.objects.all()

        data = Paginator(job, 10)
        page = request.GET.get('page')
        try:
            post = data.page(page)
        except PageNotAnInteger:
            post = data.page(1)
        except EmptyPage:
            post = data.page(data.num_pages)

        return render(request, 'view_jobs.html', {'role': role, 'username': user, 'jobs': post})
    else:
        return redirect('login')


def apply(request):
    """ Method for apply job """
    if request.session.has_key('username'):
        jobid = request.GET.get('apply')
        jobdes = request.GET.get('des')
        jobcomn = request.GET.get('cname')
        usname = request.session['username']
        app = student_info.objects.get(Enrollment=usname)
        fname = app.FirstName
        lname = app.LastName
        email = app.email
        sem = app.Semester
        bran = app.Branch
        grade = app.OverallGrade
        resume = app.Resume
        sql = job_applicant.objects.filter(JOBID=jobid, USERNAME=usname)
        if sql.count() > 0:
            messages.success(request, 'you are already apply for this job')
            return redirect('view_job')
        else:
            ap_sql = job_applicant(JOBID=jobid, COMPANYNAME=jobcomn, USERNAME=usname, FirstName=fname, LastName=lname,
                                   EMAILID=email, SEMESTER=sem, BRANCH=bran, GRADE=grade, RESUME=resume,
                                   DESIGNATION=jobdes)
            ap_sql.save()
            messages.success(request, 'successfully apply for job')
            return redirect('view_job')
    else:
        return redirect('login')


def applicant(request):
    """ Method for display applicant """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        name = company_details.objects.get(USERNAME=user)
        cname = name.COMPANYNAME

        appcant = job_applicant.objects.all().filter(COMPANYNAME=cname)

        data = Paginator(appcant, 10)
        page = request.GET.get('page')
        try:
            post = data.page(page)
        except PageNotAnInteger:
            post = data.page(1)
        except EmptyPage:
            post = data.page(data.num_pages)

        return render(request, 'view_applicants.html', {'role': role, 'username': user, 'jobs': post})
    else:
        return redirect('login')


def myaccount(request):
    """ Method for student myaccount """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']

        sdetails = student_info.objects.all().filter(USERNAME=user)
        jobdetails = job_applicant.objects.all().filter(USERNAME=user)

        return render(request, 'myaccount.html',
                      {'role': role, 'username': user, 'details': sdetails, 'jobdetails': jobdetails})
    else:
        return redirect('login')


def account(request):
    """ Method for company myaccount """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']

        comdetails = company_details.objects.all().filter(USERNAME=user)

        cname = company_details.objects.get(USERNAME=user)
        com = cname.COMPANYNAME

        jobdetails = job_details.objects.all().filter(COMPANYNAME=com)
        data = Paginator(jobdetails, 5)
        page = request.GET.get('page')
        try:
            post = data.page(page)
        except PageNotAnInteger:
            post = data.page(1)
        except EmptyPage:
            post = data.page(data.num_pages)

        return render(request, 'account.html',
                      {'role': role, 'username': user, 'comdetails': comdetails, 'jdetails': jobdetails, 'jobs': post})
    else:
        return redirect('login')


def update(request):
    """ Method for update student details """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        erno = request.GET.get('enroll')
        if request.method == 'POST':
            er = request.POST['er']
            fn = request.POST['fname']
            mn = request.POST['mname']
            ln = request.POST['lname']
            mnum = request.POST['mnum']
            email = request.POST['eid']
            dob = request.POST['dob']
            grad = request.POST['grade']

            infoupdate = student_info.objects.get(USERNAME=user)

            infoupdate.Enrollment = er
            infoupdate.FirstName = fn
            infoupdate.LastName = ln
            infoupdate.MiddleName = mn
            infoupdate.MobileNo = mnum
            infoupdate.email = email
            infoupdate.DOB = dob
            infoupdate.OverallGrade = grad

            infoupdate.save()
            return redirect('myaccount')
        else:
            sinfo = student_info.objects.all().filter(Enrollment=erno)
            return render(request, 'update.html', {'role': role, 'username': user, 'sd': sinfo})
    else:
        return redirect('login')


def company_update(request):
    """ Method for update company details """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        cname = request.GET.get('cname')
        if request.method == 'POST':
            hrname = request.POST['hrname']
            email = request.POST['email']
            link = request.POST['wl']
            cupdate = company_details.objects.get(COMPANYNAME=cname)
            cupdate.HRNAME = hrname
            cupdate.EMAILID = email
            cupdate.WEBLINK = link
            cupdate.save()
            return redirect('account')
        else:
            cinfo = company_details.objects.all().filter(COMPANYNAME=cname)
            return render(request, 'company_update.html', {'role': role, 'username': user, 'cd': cinfo})
    else:
        return redirect('login')


def changepassword(request):
    """ Method for changepassword """
    if request.session.has_key('username'):
        user = request.session['username']
        role = request.session['role']
        if request.method == 'POST':
            opsw = request.POST['opsw']
            nopsw = hashlib.md5(str.encode(opsw)).hexdigest()

            npsw = request.POST['npsw']
            cpsw = request.POST['cpsw']
            sql = login.objects.filter(USERNAME=user, PASSWORD=nopsw)
            if sql.count() > 0:
                if npsw == cpsw:
                    nnpsw = hashlib.md5(str.encode(npsw)).hexdigest()
                    chpsw = login.objects.get(USERNAME=user)
                    chpsw.PASSWORD = nnpsw
                    chpsw.save()
                    messages.error(request, 'Password Updated')
                    return redirect('change_password')
                else:
                    messages.error(request, 'Password and Confirm Password are not match')
                    return redirect('change_password')
            else:
                messages.error(request, 'Old password not match')
                return redirect('change_password')

        else:
            return render(request, 'changepassword.html', {'role': role, 'username': user})
    else:
        return redirect('login')


def canceljob(request):
    """ Method for cancel the job """
    if request.session.has_key('username'):
        jid = request.GET.get('jid')

        cjob = job_details.objects.get(id=jid)
        cname = cjob.COMPANYNAME
        japply = job_applicant.objects.get(JOBID=jid, COMPANYNAME=cname)
        japply.delete()
        cjob.delete()
        return redirect('account')
    else:
        return redirect('login')


def forgot_password(request):
    """ Method for forgot password """
    if request.method == 'POST':
        user = request.POST['username']
        sql = login.objects.filter(USERNAME=user)
        if sql.count() > 0:
            sent = request.POST['email']

            # generate 6 digit random string
            string = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyz'
            lent = len(string)
            otp = ""
            for i in range(6):
                otp += string[math.floor(random.random() * lent)]

            password = otp

            message = 'Dear ' + user + ',\n\t Your Password is: ' + otp + ',\nNote:- Can not replay on this mail'

            password = hashlib.md5(str.encode(password)).hexdigest()

            pupdate = login.objects.get(USERNAME=user)
            pupdate.PASSWORD = password
            pupdate.save()

            send_mail('TPO Portal forgot password mail', message, settings.EMAIL_HOST_USER, [sent], fail_silently=False)
            messages.error(request, 'Password send successfully.....')
            return redirect('login')
        else:
            messages.error(request, 'username is not registered..   Please register then login')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')
