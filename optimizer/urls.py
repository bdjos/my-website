from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.create_system, name='create_system'),
    path('sys_id_<str:sys_id>/add_component/', views.add_component, name='add_component'),
    path('sys_id_<str:sys_id>/view_system/', views.view_system, name='view_system'),
    path('sys_id_<str:sys_id>/run_model/', views.run_model, name='run_model'),
    path('sys_id_<str:sys_id>/add_component/add_<str:comp_type>/', views.add_system_component,
         name='add_system_component'),
    path('sys_id_<str:sys_id>/add_demand/add_<str:comp_type>/', views.add_demand, name='add_demand'),
    path('sys_id_<str:sys_id>/view_component/<str:comp_name>/', views.view_component, name='view_component'),
    path('sys_id_<str:sys_id>/view_component/<str:comp_name>/configure_controller/', views.configure_controller,
         name='configure_controller'),
    path('sys_id_<str:sys_id>/config_controller/<str:controller>/<str:comp_name>', views.add_to_controller, name='add_to_controller'),
    path('sys_id_<str:sys_id>/run_model', views.run_model, name='run_model'),
    path('sys_id_<str:sys_id>/delete_component/<str:comp_name>/', views.delete_component, name='delete_component'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
