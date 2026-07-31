from django.contrib import admin

# Register your models here.
from .models import Patient, Doctor, Appointment, Bill, Prescription, Notification

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Bill)
admin.site.register(Prescription)
admin.site.register(Notification)
