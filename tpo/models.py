from django.db import models

# Create your models here.


class login(models.Model):
    # ID = models.AutoField(primary_key=True)
    NAME = models.CharField(max_length=50)
    USERNAME = models.CharField(max_length=20, unique=True)
    PASSWORD = models.CharField(max_length=50)
    EMAILID = models.EmailField(max_length=64)
    ROLE = models.CharField(max_length=10)

    def __str__(self):
        return self.USERNAME


class company_details(models.Model):
    # ID = models.AutoField(primary_key=True)
    COMPANYNAME = models.CharField(max_length=50)
    USERNAME = models.CharField(max_length=20, unique=True)
    HRNAME = models.CharField(max_length=50)
    EMAILID = models.EmailField(max_length=64)
    ADDRESS = models.CharField(max_length=500)
    WEBLINK = models.CharField(max_length=100)

    def __str__(self):
        return self.COMPANYNAME


class job_details(models.Model):
    # JOBID = models.AutoField(primary_key=True)
    COMPANYNAME = models.CharField(max_length=50)
    DESIGNATION = models.CharField(max_length=50)
    ELIGIBILITYCRITERIA = models.CharField(max_length=25)
    JOBDESCRIPTION = models.CharField(max_length=500)

    def __str__(self):
        return self.DESIGNATION


class student_info(models.Model):
    # ID = models.AutoField(primary_key=True, unique=True)
    Enrollment = models.BigIntegerField(unique=True)
    USERNAME = models.CharField(max_length=20, unique=True)
    FirstName = models.CharField(max_length=25)
    MiddleName = models.CharField(max_length=25)
    LastName = models.CharField(max_length=25)
    MobileNo = models.BigIntegerField()
    email = models.EmailField(max_length=64)
    Semester = models.CharField(max_length=10)
    Branch = models.CharField(max_length=10)
    AdmissionYear = models.IntegerField()
    PassOutYear = models.IntegerField()
    DOB = models.DateField()
    BloodGroup = models.CharField(max_length=5)
    Gender = models.CharField(max_length=10)
    OverallGrade = models.CharField(max_length=4)
    Resume = models.FileField(upload_to='student_resume/', null=True)

    def __str__(self):
        return self.USERNAME


class job_applicant(models.Model):
    JOBID = models.IntegerField()
    COMPANYNAME = models.CharField(max_length=100)
    USERNAME = models.CharField(max_length=20)
    FirstName = models.CharField(max_length=25)
    LastName = models.CharField(max_length=25)
    EMAILID = models.EmailField(max_length=64)
    SEMESTER = models.CharField(max_length=10)
    BRANCH = models.CharField(max_length=15)
    GRADE = models.CharField(max_length=10)
    RESUME = models.FileField(upload_to='', null=True)
    DESIGNATION = models.CharField(max_length=50)

    def __str__(self):
        return self.USERNAME