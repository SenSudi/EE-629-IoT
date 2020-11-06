from django.contrib import admin
from models import Status as S
from models import Issue as I
from models import Issue_File as IF


# Register your models here.
admin.site.register(S)
admin.site.register(I)
admin.site.register(IF)
