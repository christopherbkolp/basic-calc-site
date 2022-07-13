from django import forms

class CalcForm(forms.Form):
    expression = forms.CharField(label='Calculation', max_length=200)
