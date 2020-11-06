from django.contrib import admin

# from models import Meth_Item
from models import Time_Object, Variable_Item
from models import Feedback

# from models import Report_Item, Vulnerability, Report, Recommendation
from models import Label


# Register your models here.
admin.site.register(Feedback)
admin.site.register(Label)
admin.site.register(Time_Object)
admin.site.register(Variable_Item)
