import os
import json
from datetime import datetime, timezone
import urllib.request
import urllib.parse

# Standard-Koordinaten (Waltrop)
DEFAULT_LAT = 51.6167
DEFAULT_LON = 7.3833
DEFAULT_LOCATION_NAME = "Waltrop"

# Einfache Koordinaten-Hilfe für bekannte Orte / PLZ (erweiterbar)
# Für den Start nutzen wir eine smarte Eingabe oder Standard.
# (In einer erweiterten Version kann hier ein PLZ-Lookup-Dienst angebunden werden)

def get_coordinates():
    print("==================================================")
    print("      VeritasAtmo – Interaktives Audit-System     ")
    print("==================================================")
    user_input = input(f"Gib deinen Wohnort oder deine PLZ ein (Standard: {DEFAULT_LOCATION_NAME}): ").strip()
    
    if not user_input:
        print(f"-> Keine Eingabe. Verwende Standardstandort: {DEFAULT_LOCATION_NAME}")
        return DEFAULT_LAT, DEFAULT_LON, DEFAULT_LOCATION_NAME
    
    # Kleine Erkennung für Demo-Zwecke oder manuelle Eingabe
    # Hier binden wir direkt die Geocoding-API von Open-Meteo ein (kostenlos & ohne Key!)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(user_input)}&count=1&language=de&format=json"
    
    try:
        req = urllib.request.Request(geo_url, headers={'User-Agent': 'VeritasAtmo-GeoLookup/1.0'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                geo_data = json.loads(response.read().decode('utf-8'))
                if "results" in geo_data and len(geo_data["results"]) > 0:
                    loc = geo_data["results"][0]
                    lat = loc["latitude"]
                    lon = loc["longitude"]
                    name = f"{loc.get('name')} ({loc.get('country', '')})"
                    print(f"[GEFUNDEN] Standort erfolgreich aufgelöst: {name} [Lat: {lat}, Lon: {lon}]")
                    return lat, lon, name
    except Exception as e:
        print(f"[HINWEIS] Geocoding-Fehler ({e}), falle auf Standard zurück.")
        
    print(f"-> Ort nicht automatisch gefunden. Verwende Standardstandort: {DEFAULT_LOCATION_NAME}")
    return DEFAULT_LAT, DEFAULT_LON, DEFAULT_LOCATION_NAME

def run_dashboard():
    lat, lon, location_name = get_coordinates()
    
    print(f"\n[{datetime.now(timezone.utc).isoformat()}] Starte Daten-Abruf für {location_name}...")
    
    # 1. Harvester-Schritt (Air Quality & Spurengase für den gewählten Ort)
    base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'VeritasAtmo-Dashboard/3.0'})
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"[FEHLER] Konnte Daten nicht abrufen. HTTP-Status: {response.status}")
                return
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[FEHLER beim Abruf]: {e}")
        return
        
    current = data.get("current", {})
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # 2. Werte extrahieren
    pm25 = current.get("pm2_5", 0)
    pm10 = current.get("pm10", 0)
    co = current.get("carbon_monoxide", 0)
    no2 = current.get("nitrogen_dioxide", 0)
    so2 = current.get("sulphur_dioxide", 0)
    ozone = current.get("ozone", 0)
    
    # 3. Report & Analyse ausgeben
    print("\n==================================================")
    print(f"  VeritasAtmo – Audit & Wirkungs-Bericht")
    print(f"  Standort: {location_name}")
    print(f"  Zeitstempel: {timestamp}")
    print("==================================================")
    print(f"-> Feinstaub (PM2.5): {pm25} µg/m³")
    print(f"-> Feinstaub (PM10): {pm10} µg/m³")
    print(f"-> Kohlenmonoxid (CO): {co} µg/m³")
    print(f"-> Stickstoffdioxid (NO2): {no2} µg/m³")
    print(f"-> Schwefeldioxid (SO2): {so2} µg/m³")
    print(f"-> Ozon (O3): {ozone} µg/m³")
    print("--------------------------------------------------")
    
    # 4. Wirkungs- & Hypothesen-Auswertung
    print("[ANALYSE & WIRKUNGS-PROGNOSE LAUFT...]")
    
    # Mensch-Faktor
    if ozone and ozone > 50:
        print("[MENSCH-FAKTOR]: Erhöhter photochemischer Ozon-Index.")
        print("    -> Prognose: Bei diffuser Bewölkung neigt der Körper zu verstärkter Müdigkeit, veränderten Sauerstoff-Reaktionen und Abgeschlagenheit.")
    else:
        print("[MENSCH-FAKTOR]: Spurengase unauffällig.")
        print("    -> Prognose: Hauptbelastung primär durch optischen Lichtdämpfungs-Faktor (fehlendes direktes Vollspektrum-Sonnenlicht, erhöhte Melatonin-Ausschüttung).")

    # Agrar-Faktor
    print("\n[AGRAR- & NATUR-FAKTOR]:")
    print("    -> Prognose: Indirekte Lichtstreuung begünstigt das Wachstum von Blattgemüse (z.B. Salat) auch unter trockenen Bedingungen durch reduzierte direkte Verdunstung.")
    
    print("==================================================")
    print("  Dashboard-Durchlauf erfolgreich abgeschlossen.")
    print("==================================================")

if __name__ == "__main__":
    run_dashboard()