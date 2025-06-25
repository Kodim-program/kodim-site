from django.urls import path
from psycho import views


urlpatterns = [
    path("", views.psycho),
]
