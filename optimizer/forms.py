from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CreateBattery, AddBattery, CreateSolar, AddComponent


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
        fields = ('system_capacity', 'base_cost', 'perw_cost')

class CreateGeneratorForm(forms.ModelForm):
    class Meta:
        model = CreateGenerator
        fields = ('system_capacity', 'base_cost', 'perw_cost')

class CreateGridForm(forms.ModelForm):
    class Meta:
        model = CreateSolar
        fields = ('system_capacity', 'base_cost', 'perw_cost')

class CreateControllerForm(forms.ModelForm):
    class Meta:
        model = CreateController
        fields = ('system_capacity', 'base_cost', 'perw_cost')

class AddComponentForm(forms.ModelForm):
    class Meta:
        model = AddComponent
        fields = ('comp_name', 'zone')
