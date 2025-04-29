import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import geocoding
import weather

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Météo France")
        self.root.geometry("900x700")
        self.root.minsize(900, 700)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cadre pour la recherche d'adresse
        search_frame = ttk.LabelFrame(main_frame, text="Recherche d'adresse", padding="10")
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="Adresse:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.address_entry = ttk.Entry(search_frame, width=50)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.address_entry.bind('<Return>', lambda event: self.search_address())
        
        search_button = ttk.Button(search_frame, text="Rechercher", command=self.search_address)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Cadre pour l'affichage de l'adresse et des coordonnées
        self.location_frame = ttk.LabelFrame(main_frame, text="Localisation", padding="10")
        self.location_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.location_frame, text="Adresse complète:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.full_address_var = tk.StringVar()
        ttk.Label(self.location_frame, textvariable=self.full_address_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.location_frame, text="Latitude:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.latitude_var = tk.StringVar()
        ttk.Label(self.location_frame, textvariable=self.latitude_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.location_frame, text="Longitude:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.longitude_var = tk.StringVar()
        ttk.Label(self.location_frame, textvariable=self.longitude_var).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Notebook pour afficher les prévisions
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Onglet pour les prévisions du jour
        self.today_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.today_frame, text="Aujourd'hui")
        
        # Onglet pour les prévisions de la semaine
        self.weekly_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.weekly_frame, text="Prévisions sur 5 jours")
        
    def search_address(self):
        address = self.address_entry.get().strip()
        if not address:
            messagebox.showwarning("Attention", "Veuillez entrer une adresse.")
            return
        
        try:
            # Rechercher les coordonnées avec l'API Adresse
            location_data = geocoding.get_coordinates(address)
            
            if not location_data:
                messagebox.showwarning("Erreur", "Adresse non trouvée.")
                return
            
            # Mettre à jour les informations de localisation
            self.full_address_var.set(location_data['label'])
            self.latitude_var.set(str(location_data['latitude']))
            self.longitude_var.set(str(location_data['longitude']))
            
            # Récupérer les données météo
            self.get_weather_data(location_data['latitude'], location_data['longitude'])
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite: {str(e)}")
    
    def get_weather_data(self, lat, lon):
        try:
            # Récupérer les données météo actuelles
            current_weather = weather.get_current_weather(lat, lon)
            # Récupérer les prévisions sur 5 jours
            forecast = weather.get_forecast(lat, lon)
            
            # Afficher les données
            self.display_current_weather(current_weather)
            self.display_forecast(forecast)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des données météo: {str(e)}")
    
    def display_current_weather(self, weather_data):
        # Nettoyer l'onglet des prévisions du jour
        for widget in self.today_frame.winfo_children():
            widget.destroy()
        
        # Frame d'informations principales
        info_frame = ttk.Frame(self.today_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        # Date et heure
        dt = datetime.fromtimestamp(weather_data['dt'])
        ttk.Label(info_frame, text=f"Données du {dt.strftime('%d/%m/%Y à %H:%M')}", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        
        # Ville et pays
        ttk.Label(info_frame, text=f"Lieu: {weather_data['name']}, {weather_data['sys']['country']}", font=('Helvetica', 12)).pack(anchor=tk.W)
        
        # Description de la météo
        weather_desc = weather_data['weather'][0]['description'].capitalize()
        ttk.Label(info_frame, text=f"Conditions: {weather_desc}", font=('Helvetica', 12)).pack(anchor=tk.W)
        
        # Température
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        ttk.Label(info_frame, text=f"Température: {temp}°C (Ressenti: {feels_like}°C)", font=('Helvetica', 12)).pack(anchor=tk.W)
        
        # Température min/max
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        ttk.Label(info_frame, text=f"Min: {temp_min}°C / Max: {temp_max}°C", font=('Helvetica', 12)).pack(anchor=tk.W)
        
        # Humidité et pression
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        ttk.Label(info_frame, text=f"Humidité: {humidity}% / Pression: {pressure} hPa", font=('Helvetica', 12)).pack(anchor=tk.W)
        
        # Vent
        wind_speed = weather_data['wind']['speed']
        wind_deg = weather_data['wind']['deg']
        ttk.Label(info_frame, text=f"Vent: {wind_speed} m/s, Direction: {wind_deg}°", font=('Helvetica', 12)).pack(anchor=tk.W)
        
        # Lever et coucher du soleil
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')
        ttk.Label(info_frame, text=f"Lever du soleil: {sunrise} / Coucher du soleil: {sunset}", font=('Helvetica', 12)).pack(anchor=tk.W)
    
    def display_forecast(self, forecast_data):
        # Nettoyer l'onglet des prévisions de la semaine
        for widget in self.weekly_frame.winfo_children():
            widget.destroy()
        
        # Créer un graphique pour les températures
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]})
        
        # Extraire les données pour le graphique
        times = []
        temps = []
        humidity = []
        descriptions = []
        
        # Ne prendre que les prévisions pour les 5 prochains jours (40 points de données à raison de 8 par jour)
        for item in forecast_data['list'][:40]:
            dt = datetime.fromtimestamp(item['dt'])
            times.append(dt)
            temps.append(item['main']['temp'])
            humidity.append(item['main']['humidity'])
            descriptions.append(item['weather'][0]['description'])
        
        # Graphique des températures
        ax1.plot(times, temps, 'r-', label='Température (°C)')
        ax1.set_ylabel('Température (°C)')
        ax1.set_title('Prévisions sur 5 jours')
        ax1.grid(True)
        ax1.legend()
        
        # Formater l'axe X pour qu'il soit plus lisible
        ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m %H:%M'))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Graphique de l'humidité
        ax2.plot(times, humidity, 'b-', label='Humidité (%)')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Humidité (%)')
        ax2.grid(True)
        ax2.legend()
        
        # Formater l'axe X pour qu'il soit plus lisible
        ax2.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m %H:%M'))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Créer un canvas Matplotlib dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.weekly_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Ajouter une barre d'outils de navigation (optionnel)
        toolbar_frame = ttk.Frame(self.weekly_frame)
        toolbar_frame.pack(fill=tk.X)
        toolbar = ttk.Frame(toolbar_frame)
        toolbar.pack()

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()