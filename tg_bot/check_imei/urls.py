from django.urls import path
from . import views

urlpatterns = [
    path('check-imei', views.check_imei),
]