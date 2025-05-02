from django.shortcuts import render
from .forms import LengthConversionForm, WeightConversionForm, TemperatureConversionForm

def index(request):
  return render(request, 'converter/index.html')

def convert_length(request):
  if request.method == 'POST':
    form = LengthConversionForm(request.POST)
    if form.is_valid():
      input_value = form.cleaned_data['input_value']
      input_unit = form.cleaned_data['input_unit']
      output_unit = form.cleaned_data['output_unit']
      
      # Convert to meters first (base unit)
      if input_unit == 'millimeter':
        value_in_meters = input_value / 1000
      elif input_unit == 'centimeter':
        value_in_meters = input_value / 100
      elif input_unit == 'meter':
        value_in_meters = input_value
      elif input_unit == 'kilometer':
        value_in_meters = input_value * 1000
      elif input_unit == 'inch':
        value_in_meters = input_value * 0.0254
      elif input_unit == 'foot':
        value_in_meters = input_value * 0.3048
      elif input_unit == 'yard':
        value_in_meters = input_value * 0.9144
      elif input_unit == 'mile':
        value_in_meters = input_value * 1609.344
      
      # Convert from meters to output unit
      if output_unit == 'millimeter':
        converted_value = value_in_meters * 1000
      elif output_unit == 'centimeter':
        converted_value = value_in_meters * 100
      elif output_unit == 'meter':
        converted_value = value_in_meters
      elif output_unit == 'kilometer':
        converted_value = value_in_meters / 1000
      elif output_unit == 'inch':
        converted_value = value_in_meters / 0.0254
      elif output_unit == 'foot':
        converted_value = value_in_meters / 0.3048
      elif output_unit == 'yard':
        converted_value = value_in_meters / 0.9144
      elif output_unit == 'mile':
        converted_value = value_in_meters / 1609.344
      
      return render(request, 'converter/length.html', {
        'form': form,
        'original_value': input_value,
        'original_unit': input_unit,
        'converted_value': round(converted_value, 6),
        'converted_unit': output_unit,
      })
  else:
    form = LengthConversionForm()
  
  return render(request, 'converter/length.html', {'form': form})

def convert_weight(request):
  if request.method == 'POST':
    form = WeightConversionForm(request.POST)
    if form.is_valid():
      input_value = form.cleaned_data['input_value']
      input_unit = form.cleaned_data['input_unit']
      output_unit = form.cleaned_data['output_unit']
      
      # Convert to kilograms first (base unit)
      if input_unit == 'milligram':
        value_in_kilograms = input_value / 1000000
      elif input_unit == 'gram':
        value_in_kilograms = input_value / 1000
      elif input_unit == 'kilogram':
        value_in_kilograms = input_value
      elif input_unit == 'ounce':
        value_in_kilograms = input_value * 0.0283495
      elif input_unit == 'pound':
        value_in_kilograms = input_value * 0.453592
      
      # Convert from kilograms to output unit
      if output_unit == 'milligram':
        converted_value = value_in_kilograms * 1000000
      elif output_unit == 'gram':
        converted_value = value_in_kilograms * 1000
      elif output_unit == 'kilogram':
        converted_value = value_in_kilograms
      elif output_unit == 'ounce':
        converted_value = value_in_kilograms / 0.0283495
      elif output_unit == 'pound':
        converted_value = value_in_kilograms / 0.453592
      
      return render(request, 'converter/weight.html', {
        'form': form,
        'original_value': input_value,
        'original_unit': input_unit,
        'converted_value': round(converted_value, 6),
        'converted_unit': output_unit,
      })
  else:
    form = WeightConversionForm()
    
  return render(request, 'converter/weight.html', {'form': form})

def convert_temperature(request):
  if request.method == 'POST':
    form = TemperatureConversionForm(request.POST)
    if form.is_valid():
      input_value = form.cleaned_data['input_value']
      input_unit = form.cleaned_data['input_unit']
      output_unit = form.cleaned_data['output_unit']
      
      # Convert to Celsius first (base unit)
      if input_unit == 'celsius':
        value_in_celsius = input_value
      elif input_unit == 'fahrenheit':
        value_in_celsius = (input_value - 32) * 5/9
      elif input_unit == 'kelvin':
        value_in_celsius = input_value - 273.15
      
      # Convert from Celsius to output unit
      if output_unit == 'celsius':
        converted_value = value_in_celsius
      elif output_unit == 'fahrenheit':
        converted_value = (value_in_celsius * 9/5) + 32
      elif output_unit == 'kelvin':
        converted_value = value_in_celsius + 273.15
      
      return render(request, 'converter/temperature.html', {
        'form': form,
        'original_value': input_value,
        'original_unit': input_unit,
        'converted_value': round(converted_value, 6),
        'converted_unit': output_unit,
      })
  else:
    form = TemperatureConversionForm()
  
  return render(request, 'converter/temperature.html', {'form': form})