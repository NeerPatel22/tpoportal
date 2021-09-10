from django.contrib import admin
from .models import login, company_details, job_details, job_applicant, student_info
# Register your models here.
admin.site.register(login)
admin.site.register(company_details)
admin.site.register(job_details)
admin.site.register(job_applicant)
admin.site.register(student_info)