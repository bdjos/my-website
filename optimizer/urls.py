from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_component/', views.add_component, name='add_component'),
    path('run_model/', views.run_model, name='run_model'),
    path('add_component/add_demand/', views.add_demand, name='add_demand'),
    path('add_component/add_demand/', views.add_demand, name='add_solar'),
    path('add_component/add_battery/', views.add_battery, name='add_battery'),
    path('add_component/add_demand/', views.add_demand, name='add_converter'),
    path('add_component/add_demand/', views.add_demand, name='add_generator'),
    path('add_component/add_demand/', views.add_demand, name='add_controller'),
    path('add_component/add_demand/', views.add_demand, name='add_grid'),
]
