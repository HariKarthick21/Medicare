from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('department/', views.department, name='department'),
    path('doctor/', views.doctor, name='doctor'),
    path('appointment/', views.appointment, name='appointment'),
    path('registration/', views.registration, name='registration'),
    path('contact/', views.contact, name='contact'),
    path('get-slots/', views.get_slots, name='get_slots'),
]