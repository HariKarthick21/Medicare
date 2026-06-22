from django.db import models
from django.core.validators import MinValueValidator

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_description = models.TextField()

    def __str__(self):
        return self.department_name

class Doctor(models.Model):
    doctor_name = models.CharField(max_length=100)
    doctor_specialization = models.CharField(max_length=100)
    doctor_image = models.ImageField(upload_to='doctors/')
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    available_from = models.TimeField()
    available_to = models.TimeField()
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)
    def __str__(self):
        return self.doctor_name

class Patient(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_age = models.IntegerField(validators=[MinValueValidator(1)])
    patient_phone = models.CharField(max_length=10)
    patient_email = models.EmailField()
    patient_problem = models.TextField()

    def __str__(self):
        return self.patient_name

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor_name = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    def __str__(self):
        return f"{self.patient_name} - {self.doctor_name}"