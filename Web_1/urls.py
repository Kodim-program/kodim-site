from django.urls import path, include
from Web_1 import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name = 'courses'),
    path('course/<int:id>/', views.course, name = 'course'),
]