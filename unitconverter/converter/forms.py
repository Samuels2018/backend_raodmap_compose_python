from django import forms

class LengthConversionForm(forms.Form):
  MEASUREMENTS = [
    ('millimeter', 'Millimeter'),
    ('centimeter', 'Centimeter'),
    ('meter', 'Meter'),
    ('kilometer', 'Kilometer'),
    ('inch', 'Inch'),
    ('foot', 'Foot'),
    ('yard', 'Yard'),
    ('mile', 'Mile'),
  ]
    
  input_value = forms.DecimalField(label='Value to convert')
  input_unit = forms.ChoiceField(label='From', choices=MEASUREMENTS)
  output_unit = forms.ChoiceField(label='To', choices=MEASUREMENTS)

class WeightConversionForm(forms.Form):
  MEASUREMENTS = [
    ('milligram', 'Milligram'),
    ('gram', 'Gram'),
    ('kilogram', 'Kilogram'),
    ('ounce', 'Ounce'),
    ('pound', 'Pound'),
  ]
    
  input_value = forms.DecimalField(label='Value to convert')
  input_unit = forms.ChoiceField(label='From', choices=MEASUREMENTS)
  output_unit = forms.ChoiceField(label='To', choices=MEASUREMENTS)

class TemperatureConversionForm(forms.Form):
  MEASUREMENTS = [
    ('celsius', 'Celsius'),
    ('fahrenheit', 'Fahrenheit'),
    ('kelvin', 'Kelvin'),
  ]
  
  input_value = forms.DecimalField(label='Value to convert')
  input_unit = forms.ChoiceField(label='From', choices=MEASUREMENTS)
  output_unit = forms.ChoiceField(label='To', choices=MEASUREMENTS)