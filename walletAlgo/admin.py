from django.contrib import admin
from .models import user
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Register your models here.
admin.site.register(user,UserAdmin)
admin.site.unregister(Group)

UserAdmin.fieldsets += ("Custome field set",{'fields':('passfrase','Address','privateKey',)}),