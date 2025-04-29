from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('length/', views.convert_length, name='length'),
  path('weight/', views.convert_weight, name='weight'),
  path('temperature/', views.convert_temperature, name='temperature'),
]