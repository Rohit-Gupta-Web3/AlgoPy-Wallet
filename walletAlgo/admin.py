from django.contrib import admin
from .models import user
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(user,UserAdmin)

UserAdmin.fieldsets += ("Custome field set",{'fields':('passfrase','Address','privateKey',)}),