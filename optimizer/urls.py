from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_component/', views.add_component, name='add_component'),
    path('add_component/add_demand/', views.add_demand, name='add_demand')
]
