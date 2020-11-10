from django.contrib import admin
from models import Project as P
from models import Milestone as M
from models import Vip as V


# Register your models here.
admin.site.register(P)
admin.site.register(M)
admin.site.register(V)
