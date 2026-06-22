from django import forms
from .models import Patient, Appointment
import re

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_email': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'patient_problem': forms.Textarea(attrs={'class': 'form-control'}),
        }

    # ✅ Name validation (only alphabets)
    def clean_patient_name(self):
        name = self.cleaned_data['patient_name'].strip()
        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError("Name should contain only alphabets.")
        return name

    # ✅ Age validation (not less than 1)
    def clean_patient_age(self):
        age = self.cleaned_data['patient_age']
        if age < 1:
            raise forms.ValidationError("Age must be greater than 0.")
        return age

    # ✅ Phone validation (only numbers, 10 digits)
    def clean_patient_phone(self):
        phone = self.cleaned_data['patient_phone']
        if not phone.isdigit():
            raise forms.ValidationError("Phone must contain only numbers.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone must be 10 digits.")
        return phone

    # ✅ Email validation (@ check is default, but extra safe)
    def clean_patient_email(self):
        email = self.cleaned_data['patient_email']
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Invalid email format.")
        return email

    # ✅ Problem validation (minimum 5 words)
    def clean_patient_problem(self):
        problem = self.cleaned_data['patient_problem'].strip()
        if len(problem.split()) < 5:
            raise forms.ValidationError("Please describe problem in at least 5 words.")
        return problem

import datetime
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor_name': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': datetime.date.today().isoformat()
            }, format='%Y-%m-%d'),

            'appointment_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }, format='%H:%M'),
        }