import os
import json
from datetime import datetime, timezone
import urllib.request
import urllib.parse

# Koordinaten für Waltrop
LATITUDE = 51.6167
LONGITUDE = 7.3833

# Wir rufen jetzt die Open-Meteo Air Quality API ab, um Spurengase & Umweltwerte zu erfassen
BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
    "hourly": "carbon_monoxide,nitrogen_dioxide"
}
URL = f"{BASE_URL}?{urllib.parse.urlencode(params)}"

def fetch_atmosphere_data():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starte CO₂- & Spurengas-Abruf für Waltrop (Air Quality Harvester)...")
    
    try:
        req = urllib.request.Request(
            URL, 
            headers={'User-Agent': 'VeritasAtmo-AirQualityHarvester/2.3'}
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                
                payload = {
                    "fetch_timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "source": "Open-Meteo Air Quality API (Zero-Key Harvester)",
                    "coordinates": {"lat": LATITUDE, "lon": LONGITUDE},
                    "raw_data": data
                }
                
                filename = "atmphaeren_rohdaten.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False, indent=4)
                    
                print(f"[ERFOLG] Spurengas- & Umweltrohdaten erfolgreich in '{filename}' gesichert.")
                return payload
            else:
                print(f"[FEHLER] HTTP-Statuscode: {response.status}")
                return None
    except Exception as e:
                print(f"[FEHLER beim Abruf]: {e}")
                return None

if __name__ == "__main__":
    fetch_atmosphere_data()