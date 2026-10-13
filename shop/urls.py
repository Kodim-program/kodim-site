from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path("models/", views.catalog, name="models_catalog"),
    path("models/<slug:slug>/", views.model_detail, name="model_detail"),
    path("services/", views.services_catalog, name="services_catalog"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
]