from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CreateBattery, AddBattery


class CreateBatteryForm(forms.ModelForm):
    class Meta:
        model = CreateBattery
        fields = ('energy_capacity', 'soc_min', 'soc_max', 'base_cost', 'energy_cost')

class AddBatteryForm(forms.ModelForm):
    class Meta:
        model = AddBattery
        fields = ('bat_name', 'zone')
