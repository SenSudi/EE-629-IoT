from django.contrib import admin

from models import Report_Item
from models import Report_Item_Type
from models import Report_Item_Attribute
from models import Wizard_Step
from models import Wizard_Template
from models import Report_Variable
from models import Wizard_Variable
from models import Report
from models import Static_Attribute

# Register your models here.
admin.site.register(Report_Item)
admin.site.register(Wizard_Step)
admin.site.register(Wizard_Template)
admin.site.register(Report_Variable)
admin.site.register(Wizard_Variable)
admin.site.register(Report)
admin.site.register(Report_Item_Type)
admin.site.register(Report_Item_Attribute)
admin.site.register(Static_Attribute)
