from django.contrib import admin
from .models import Wing, Flat, ParkingSlot, Notice, EmergencyContact

admin.site.register(Wing)
admin.site.register(Flat)
admin.site.register(ParkingSlot)
admin.site.register(Notice)
admin.site.register(EmergencyContact)
