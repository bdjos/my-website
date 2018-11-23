import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class AddSolar(forms.Form):
    solar_size = forms.IntegerField(help_text="Enter a system size between 1 and 1000 kW")
    solar_size = forms.IntegerField(help_text="Enter a system size between 1 and 1000 kW")
    solar_size = forms.IntegerField(help_text="Enter a system size between 1 and 1000 kW")

    def clean_renewal_date(self):

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
