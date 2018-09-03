from .models import SalesforceFile
from django import forms
from bootstrap_daterangepicker import widgets, fields


class SalesforceFileForm(forms.ModelForm):
 
    # Date Range Fields
    date_range_with_format = fields.DateRangeField(input_formats=['%d/%m/%Y'],widget=widgets.DateRangeWidget(format='%d/%m/%Y'))


    class Meta:
        model = SalesforceFile
        fields = ['date_range_with_format']