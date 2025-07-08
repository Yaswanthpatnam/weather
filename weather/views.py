from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def index(request):
    return render(request, 'weather/index.html')

def get_weather(request):
    if request.method == 'POST':
        city = request.POST.get('city').strip()  # Remove unwanted spaces

        if not city:
            return render(request, 'weather/index.html', {'error': "Please enter a city name."})

        try:
            request_url = f"{BASE_URL}?q={city}&appid={API_KEY}"
            response = requests.get(request_url)

            if response.status_code == 200:
                data = response.json()
                weather = data["weather"][0]["description"].title()
                temperature = round(data["main"]["temp"] - 273.15, 2)

                context = {
                    'city': city,
                    'weather': weather,
                    'temperature': temperature
                }
                return render(request, 'weather/result.html', context)

            elif response.status_code == 404:
                return render(request, 'weather/index.html', {'error': f"City '{city}' not found."})
            else:
                return render(request, 'weather/index.html', {'error': "Something went wrong. Please try again later."})

        except requests.exceptions.RequestException as e:
            print("Exception:", e)
            return render(request, 'weather/index.html', {'error': "Network error. Please check your connection."})

    return render(request, 'weather/index.html')
