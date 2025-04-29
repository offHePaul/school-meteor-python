"""
Module pour l'interaction avec l'API OpenWeatherMap
https://openweathermap.org/api
"""

import requests
import json
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# URLs de base pour les APIs OpenWeatherMap
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_current_weather(lat, lon, lang="fr", units="metric"):
    """
    Récupère les données météorologiques actuelles pour une localisation donnée.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        lang (str): Code de langue (fr pour français)
        units (str): Unités (metric pour Celsius)
        
    Returns:
        dict: Données météorologiques actuelles
    """
    try:
        # Vérifier que la clé API est disponible
        if not API_KEY:
            raise ValueError("La clé API OpenWeatherMap n'est pas définie. Veuillez définir la variable d'environnement OPENWEATHERMAP_API_KEY.")
        
        # Préparer les paramètres de requête
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "lang": lang,
            "units": units
        }
        
        # Effectuer la requête
        response = requests.get(CURRENT_WEATHER_URL, params=params)
        response.raise_for_status()  # Lever une exception en cas d'erreur HTTP
        
        # Retourner les données météo
        return response.json()
        
    except Exception as e:
        print(f"Erreur lors de la récupération des données météo actuelles: {str(e)}")
        raise e

def get_forecast(lat, lon, lang="fr", units="metric"):
    """
    Récupère les prévisions météorologiques sur 5 jours pour une localisation donnée.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        lang (str): Code de langue (fr pour français)
        units (str): Unités (metric pour Celsius)
        
    Returns:
        dict: Données des prévisions météorologiques
    """
    try:
        # Vérifier que la clé API est disponible
        if not API_KEY:
            raise ValueError("La clé API OpenWeatherMap n'est pas définie. Veuillez définir la variable d'environnement OPENWEATHERMAP_API_KEY.")
        
        # Préparer les paramètres de requête
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "lang": lang,
            "units": units
        }
        
        # Effectuer la requête
        response = requests.get(FORECAST_URL, params=params)
        response.raise_for_status()  # Lever une exception en cas d'erreur HTTP
        
        # Retourner les données des prévisions
        return response.json()
        
    except Exception as e:
        print(f"Erreur lors de la récupération des prévisions météo: {str(e)}")
        raise e

def get_weather_icon_url(icon_code):
    """
    Génère l'URL pour récupérer l'icône météo.
    
    Args:
        icon_code (str): Code de l'icône fourni par OpenWeatherMap
        
    Returns:
        str: URL de l'icône
    """
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

# Pour tester le module directement
if __name__ == "__main__":
    if not API_KEY:
        print("Erreur: La clé API OpenWeatherMap n'est pas définie.")
        print("Veuillez créer un fichier .env contenant: OPENWEATHERMAP_API_KEY=votre_clé_api")
    else:
        # Coordonnées de Paris
        lat = 48.8566
        lon = 2.3522
        
        try:
            # Tester la récupération des données météo actuelles
            weather_data = get_current_weather(lat, lon)
            print("Données météo actuelles:")
            print(f"Ville: {weather_data['name']}")
            print(f"Température: {weather_data['main']['temp']}°C")
            print(f"Description: {weather_data['weather'][0]['description']}")
            
            # Tester la récupération des prévisions
            forecast_data = get_forecast(lat, lon)
            print("\nPrévisions:")
            for item in forecast_data['list'][:3]:  # Afficher les 3 premières prévisions
                print(f"Date: {item['dt_txt']}")
                print(f"Température: {item['main']['temp']}°C")
                print(f"Description: {item['weather'][0]['description']}")
                print("-" * 30)
                
        except Exception as e:
            print(f"Erreur lors du test: {str(e)}")