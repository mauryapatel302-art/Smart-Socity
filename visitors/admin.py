from django.contrib import admin
from .models import VisitorLog, GatePassRequest

admin.site.register(VisitorLog)
admin.site.register(GatePassRequest)
