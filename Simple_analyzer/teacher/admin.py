from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class Teacheradmin(UserAdmin):
    model=Teacher
    fieldsets=UserAdmin.fieldsets+(
        ('Additional Information',{'fields':('contact',)}),
    )

admin.site.register(Teacher,Teacheradmin)
admin.site.register(Student)
admin.site.register(Stream)
admin.site.register(Marks)
admin.site.register(Subject)
