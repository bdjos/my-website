from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_component/', views.add_component, name='add_component'),
    path('run_model/', views.run_model, name='run_model'),
    path('add_component/add_demand/', views.add_demand, name='add_demand'),
    path('add_component/add_solar/', views.add_solar, name='add_solar'),
    path('add_component/add_battery/', views.add_battery, name='add_battery'),
    path('add_component/add_converter/', views.add_converter, name='add_converter'),
    path('add_component/add_generator/', views.add_generator, name='add_generator'),
    path('add_component/add_solar/', views.add_solar, name='add_controller'),
    path('add_component/add_grid/', views.add_grid, name='add_grid'),
]
