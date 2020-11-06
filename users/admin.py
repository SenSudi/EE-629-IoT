from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from models import Context

from models import Tester

# Register your models here.
class TesterInline(admin.StackedInline):
    model = Tester
    can_delete = False
    verbose_name_plural = "testers"


class UserAdmin(BaseUserAdmin):
    inlines = (TesterInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Context)
