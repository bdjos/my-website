from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CreateBattery


class CreateBatteryForm(forms.ModelForm):
    class Meta:
        model = CreateBattery
        fields = ('bat_name', 'energy_capacity', 'soc_min', 'soc_max', 'base_cost', 'energy_cost')
