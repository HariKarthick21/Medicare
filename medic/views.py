from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Department, Patient, Appointment, Doctor
from .forms import PatientForm, AppointmentForm
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def department(request):
    departments = Department.objects.all()
    return render(request, 'department.html', {'departments': departments})

def doctor(request):
    departments = Department.objects.all()
    return render(request, 'doctor.html', {'departments': departments})

def registration(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient registered successfully ✅")
            form = PatientForm()
        else:
            messages.error(request, "Please correct the errors below ❌")
    else:
        form = PatientForm()

    return render(request, 'registration.html', {'form': form})

def appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data.get('doctor_name')
            appointment_date = form.cleaned_data.get('appointment_date')

            from datetime import datetime
            time_str = request.POST.get('appointment_time')
            appointment_time = datetime.strptime(time_str, "%I:%M %p").time()
            form.instance.appointment_time = appointment_time

            # ✅ Check doctor working hours
            if appointment_time < doctor.available_from or appointment_time > doctor.available_to:
                messages.error(
                    request,
                    f"Doctor available only between {doctor.available_from} - {doctor.available_to}"
                )
                return redirect('appointment')

            # 🚫 NEW: Check break time
            if doctor.break_start and doctor.break_end:
                if doctor.break_start <= appointment_time < doctor.break_end:
                    messages.error(
                        request,
                        f"Doctor not available during break ({doctor.break_start} - {doctor.break_end})"
                    )
                    return redirect('appointment')

            # 🚫 Prevent double booking
            already_booked = Appointment.objects.filter(
                doctor_name=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            ).exists()

            if already_booked:
                messages.error(request, "This time slot is already booked!")
                return redirect('appointment')

            form.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('appointment')
    else:
        form = AppointmentForm()

    return render(request, 'appointment.html', {'form': form})

def contact(request):
    return render(request, 'contact.html')

def get_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')
    if not doctor_id or not date:
        return JsonResponse({'slots': []})
    doctor = Doctor.objects.get(id=doctor_id)
    start = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), doctor.available_from)
    end = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), doctor.available_to)
    now = timezone.localtime()
    slots = []
    while start < end:
        current_time = start.time()
        # ⏳ Block past time (today only)
        if date == now.strftime("%Y-%m-%d"):
            if current_time <= now.time():
                start += timedelta(minutes=30)
                continue
        # 🚫 Skip break time
        if doctor.break_start and doctor.break_end:
            if doctor.break_start <= current_time < doctor.break_end:
                start += timedelta(minutes=30)
                continue
        slots.append(current_time.strftime("%I:%M %p"))
        start += timedelta(minutes=30)
    # 🚫 Remove booked slots
    booked = Appointment.objects.filter(
        doctor_name=doctor,
        appointment_date=date
    ).values_list('appointment_time', flat=True)
    booked_slots = [t.strftime("%H:%M") for t in booked]
    # 🎨 Return status
    slot_data = []
    for slot in slots:
        if slot in booked_slots:
            status = "booked"
        else:
            status = "available"
        slot_data.append({
            "time": slot,
            "status": status
        })
    return JsonResponse({'slots': slot_data})