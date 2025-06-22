from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import RegisterForm
from .models import Course, CO, PO, COPOMapping, COAttainment

class CustomUserAdmin(BaseUserAdmin):
    add_form = RegisterForm

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(CO)
admin.site.register(PO)
admin.site.register(COPOMapping)
admin.site.register(COAttainment)
