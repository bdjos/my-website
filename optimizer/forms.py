from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CreateDemand, CreateBattery, CreateSolar, CreateConverter, CreateController, CreateGrid, CreateGenerator, AddComponent, AddToController


class CreateDemandForm(forms.ModelForm):
    class Meta:
        model = CreateDemand
        fields = ('demand',)

class CreateBatteryForm(forms.ModelForm):
    class Meta:
        model = CreateBattery
        fields = ('energy_capacity', 'soc_min', 'soc_max', 'base_cost', 'energy_cost')

class CreateSolarForm(forms.ModelForm):
    class Meta:
        model = CreateSolar
        fields = ('system_capacity', 'base_cost', 'perw_cost')

class CreateConverterForm(forms.ModelForm):
    class Meta:
        model = CreateConverter
        fields = ('power', 'base_cost', 'power_cost')

class CreateGeneratorForm(forms.ModelForm):
    class Meta:
        model = CreateGenerator
        fields = ('power', 'base_cost', 'fuel_cost')

class CreateGridForm(forms.ModelForm):
    ###### Grid needs to be updated
    class Meta:
        model = CreateGrid
        fields = ('energy_cost', 'nm_allowed')

class CreateControllerForm(forms.ModelForm):
    class Meta:
        model = CreateController
        fields = ()

class AddComponentForm(forms.ModelForm):
    class Meta:
        model = AddComponent
        fields = ('comp_name',)

class AddToControllerForm(forms.ModelForm):
    class Meta:
        model = AddToController
        fields = ('mode',)
