from django.contrib import admin
from .models import MaintenanceBill, Payment

admin.site.register(MaintenanceBill)
admin.site.register(Payment)
