from django.urls import path

from .views import header_pages

urlpatterns = [
    path('', header_pages.index, name='index'),
    path('add_component/', header_pages.add_component, name='add_component'),
    path('run_model/', header_pages.run_model, name='run_model'),
    path('add_component/add_demand/', header_pages.add_demand, name='add_demand'),
    path('add_component/add_demand/', header_pages.add_demand, name='add_solar'),
    path('add_component/add_battery/', header_pages.add_battery, name='add_battery'),
    path('add_component/add_demand/', header_pages.add_demand, name='add_converter'),
    path('add_component/add_demand/', header_pages.add_demand, name='add_generator'),
    path('add_component/add_demand/', header_pages.add_demand, name='add_controller'),
    path('add_component/add_demand/', header_pages.add_demand, name='add_grid'),
]
