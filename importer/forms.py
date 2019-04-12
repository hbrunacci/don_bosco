from .models import SalesforceFile, Sf_Ids
from django import forms
from bootstrap_daterangepicker import widgets, fields


class SalesforceFileForm(forms.ModelForm):
 
    # Date Range Fields
    date_range_with_format = fields.DateRangeField(input_formats=['%d/%m/%Y'], widget=widgets.DateRangeWidget(format='%d/%m/%Y'))
    date_range_with_format.label= 'Rango de Fechas'
    class Meta:
        model = SalesforceFile
        fields = ['date_range_with_format']


class UnidentifiedForm(forms.ModelForm):

    class Meta:
        model = Sf_Ids
        fields = ['partner_id', 'sf_partner_id', ]