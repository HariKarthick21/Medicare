from django.contrib import admin
from .models import Department, Doctor, Appointment

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name', 'department_description')
    search_fields = ('department_name',)
admin.site.register(Department, DepartmentAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor_name', 'doctor_specialization', 'department_name')
    list_filter = ('department_name',)
    search_fields = ('doctor_name',)
admin.site.register(Doctor, DoctorAdmin)

admin.site.register(Appointment)