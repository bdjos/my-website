from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ieso_predict/', views.ieso_predict, name='ieso_predict')
]
