from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CreateSystem, CreateDemand, CreateBattery, CreateSolar, CreateConverter, \
    CreateController, CreateGrid, CreateGenerator, AddComponent, AddToController


def create_component_form(comp_type):
    models = {
            'system': {'model': CreateSystem, 'fields': ('system_name',)},
            'demand': {'model': CreateDemand, 'fields': ('demand_file',)},
            'battery': {'model': CreateBattery, 'fields': ('energy_capacity', 'soc_min', 'soc_max', 'efficiency',
                                                           'base_cost', 'energy_cost')},
            'solar': {'model': CreateSolar, 'fields': ('system_capacity', 'base_cost', 'perw_cost')},
            'generator': {'model': CreateGenerator, 'fields': ('power', 'base_cost', 'fuel_cost')},
            'converter': {'model': CreateConverter, 'fields': ('power', 'base_cost', 'power_cost')},
            'controller': {'model': CreateController, 'fields': ()},
            'grid': {'model': CreateGrid, 'fields': ('energy_cost', 'nm_allowed')},
            }
    comp_spec = models[comp_type]

    class CreateForm(forms.ModelForm):
        class Meta:
            model = comp_spec['model']
            fields = comp_spec['fields']
    return CreateForm


class CreateSystemForm(forms.ModelForm):
    class Meta:
        model = CreateSystem
        fields = ('system_name',)


class AddToControllerForm(forms.ModelForm):
    class Meta:
        model = AddToController
        fields = ('mode',)
