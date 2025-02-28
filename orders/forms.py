# forms.py
from django import forms

class TableSearchForm(forms.Form):
    table_number = forms.IntegerField(label='Номер стола', min_value=1)