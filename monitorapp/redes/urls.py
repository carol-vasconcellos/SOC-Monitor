from django.urls import path
from . import views

urlpatterns = [
    path('', views.monitor_redes, name='monitor_redes'),
]
