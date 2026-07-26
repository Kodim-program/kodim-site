from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.my_courses, name='my_courses'),
    path('course/<int:course_id>/', views.course_materials, name='course_materials'),
    path('material/<int:material_id>/', views.material_detail, name='material_detail'),
    path('course/<int:course_id>/test/', views.take_test, name='take_test'),
    path('course/<int:course_id>/test/result/', views.test_result, name='test_result'),
]
