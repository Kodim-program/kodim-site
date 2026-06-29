from django.urls import path
from projects import views


urlpatterns = [
    path("", views.projects),
    path("summer/", views.projects_summer),
    path("miami/", views.projects_miami),
    path('memory/', views.memory_project),
    path('easter/', views.project_easter),
    path('pillows/', views.project_pillows),
    path('sakura_soul/', views.project_sakura_soul),
    path('cosmos/', views.project_cosmos),
]
