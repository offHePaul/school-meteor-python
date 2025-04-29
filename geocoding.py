"""
Module pour l'interaction avec l'API Adresse du gouvernement français
https://adresse.data.gouv.fr/api-doc/adresse
"""

import requests
import json

# URL de base pour l'API Adresse
API_ADRESSE_URL = "https://api-adresse.data.gouv.fr/search/"

def get_coordinates(address):
    """
    Récupère les coordonnées géographiques d'une adresse en utilisant l'API Adresse.
    
    Args:
        address (str): L'adresse à rechercher
        
    Returns:
        dict: Dictionnaire contenant les informations de localisation (label, latitude, longitude)
        None: Si aucune adresse n'est trouvée
    """
    try:
        # Préparer les paramètres de la requête
        params = {
            "q": address,
            "limit": 1  # Limiter à 1 résultat
        }
        
        # Effectuer la requête
        response = requests.get(API_ADRESSE_URL, params=params)
        response.raise_for_status()  # Lever une exception en cas d'erreur HTTP
        
        # Analyser la réponse JSON
        data = response.json()
        
        # Vérifier si des résultats ont été trouvés
        if data["features"] and len(data["features"]) > 0:
            feature = data["features"][0]
            properties = feature["properties"]
            coordinates = feature["geometry"]["coordinates"]
            
            # Retourner les données formatées
            return {
                "label": properties["label"],
                "city": properties.get("city", ""),
                "postcode": properties.get("postcode", ""),
                "latitude": coordinates[1],  # Latitude (y)
                "longitude": coordinates[0]  # Longitude (x)
            }
        else:
            return None
            
    except Exception as e:
        print(f"Erreur lors de la recherche d'adresse: {str(e)}")
        raise e

def get_suggestions(query, limit=5):
    """
    Obtient des suggestions d'adresses pour l'autocomplétion.
    
    Args:
        query (str): La requête de recherche partielle
        limit (int): Le nombre maximum de suggestions à retourner
        
    Returns:
        list: Liste des suggestions d'adresses
    """
    try:
        # URL pour l'autocomplétion
        url = "https://api-adresse.data.gouv.fr/search/"
        
        # Paramètres de requête
        params = {
            "q": query,
            "limit": limit,
            "autocomplete": 1
        }
        
        # Effectuer la requête
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Analyser la réponse
        data = response.json()
        
        # Extraire les labels des suggestions
        suggestions = []
        if "features" in data:
            for feature in data["features"]:
                suggestions.append(feature["properties"]["label"])
                
        return suggestions
        
    except Exception as e:
        print(f"Erreur lors de la récupération des suggestions: {str(e)}")
        return []

# Pour tester le module directement
if __name__ == "__main__":
    # Test de la fonction get_coordinates
    test_address = "55 Rue du Faubourg Saint-Honoré, Paris"
    result = get_coordinates(test_address)
    
    if result:
        print(f"Adresse: {result['label']}")
        print(f"Latitude: {result['latitude']}")
        print(f"Longitude: {result['longitude']}")
    else:
        print("Adresse non trouvée.")
        
    # Test de la fonction get_suggestions
    test_query = "55 rue du"
    suggestions = get_suggestions(test_query)
    
    print("\nSuggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")