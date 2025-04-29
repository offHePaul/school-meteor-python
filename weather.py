# weather.py
import requests
from config import API_KEY, API_URL

def fetch_weather(city: str):
    if not city:
        return None, "Veuillez entrer un nom de ville."

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'fr'
    }

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return None, f"Erreur : {data.get('message', 'Ville introuvable')}"

        weather = {
            'description': data['weather'][0]['description'].capitalize(),
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon']
        }

        return weather, None

    except Exception as e:
        return None, str(e)
