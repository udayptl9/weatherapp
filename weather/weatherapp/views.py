from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&APPID=66893c453d6e4c4a5ab7b91847978075'

    if request.method == "POST":
        form = CityForm(request.POST)
        cities = City.objects.order_by('-id')
        for city in cities:
            enter = request.POST.get('name')
            if enter == city.name:
                messages.error(request, 'City name already existed')
                return redirect('weather')
            else:
                r = requests.get(url.format(enter)).json()
                if(r['cod'] == '404'):
                    messages.error(request, 'Enter a valid city name')
                    return redirect('weather')
                else:
                    form.save()
                    messages.success(request, 'City has been added to database')
                    return redirect('weather')
    form = CityForm()

    cities = City.objects.order_by('-id')
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weatherapp/weather.html', context)


def delete(request, cityId):
    City.objects.get(pk=cityId).delete()
    messages.error(request, 'Deleted Successfully')
    return redirect('weather')
