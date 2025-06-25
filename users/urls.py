from django.urls import path, include
from users import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.Register.as_view(), name = 'registration'),
    path('profile/', views.profile, name = 'profile'),
]