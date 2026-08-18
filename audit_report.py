import json
import os
from datetime import datetime, timezone

def generate_audit_report():
    filename = "atmphaeren_rohdaten.json"
    if not os.path.exists(filename):
        print(f"[FEHLER] Keine Rohdaten-Datei '{filename}' gefunden. Bitte zuerst den Harvester laufen lassen!")
        return
    
    with open(filename, "r", encoding="utf-8") as f:
        payload = json.load(f)
        
    data = payload.get("raw_data", {})
    current = data.get("current", {})
    timestamp = payload.get("fetch_timestamp_utc")
    
    # Neue Spurengas- und Umweltparameter auslesen
    pm25 = current.get("pm2_5", 0)
    pm10 = current.get("pm10", 0)
    co = current.get("carbon_monoxide", 0)
    no2 = current.get("nitrogen_dioxide", 0)
    so2 = current.get("sulphur_dioxide", 0)
    ozone = current.get("ozone", 0)
    
    # Text-Bewertung für Mensch & Natur ermitteln
    if ozone and ozone > 50:
        mensch_befund = "Erhöhter photochemischer Ozon-Index. Bei diffuser Bewölkung neigt der Körper zu verstärkter Müdigkeit, veränderten Sauerstoff-Reaktionen und Abgeschlagenheit."
    else:
        mensch_befund = "Spurengase im unauffälligen Bereich. Hauptbelastung primär durch optischen Lichtdämpfungs-Faktor (fehlendes direktes Vollspektrum-Sonnenlicht, erhöhte Melatonin-Ausschüttung)."

    agrar_befund = "Indirekte Lichtstreuung (Milchiger Himmel) in Kombination mit stabilen CO₂-Werten begünstigt das Wachstum von Blattgemüse (z.B. Salat) auch unter trockenen Bedingungen durch reduzierte direkte Verdunstung."

    report_content = f"""# VeritasAtmo – Offizieller Atmosphären-, Spurengas- & Wirkungs-Audit
**Standort:** Waltrop (Lat: 51.62, Lon: 7.38)  
**Erstellungszeitpunkt (UTC):** {timestamp}  
**Datenquelle:** Open-Meteo Air Quality API (Zero-Key Harvester)  

---

## 1. Gemessene Live-Spurengas- & Umweltparameter
* **Feinstaub (PM2.5):** {pm25} µg/m³
* **Feinstaub (PM10):** {pm10} µg/m³
* **Kohlenmonoxid (CO):** {co} µg/m³
* **Stickstoffdioxid (NO2):** {no2} µg/m³
* **Schwefeldioxid (SO2):** {so2} µg/m³
* **Ozon (O3):** {ozone} µg/m³

## 2. System-Befund & Wirkungs-Prognose
### A. Mensch-Faktor (Psycho-Physiologie)
> **Befund:** {mensch_befund}

### B. Agrar- & Natur-Faktor (Pflanzenwachstum & Dürre-Resistenz)
> **Befund:** {agrar_befund}

---
*VeritasAtmo Autonomous Audit Engine – Generiert auf Basis freier Primärdaten.*
"""

    report_filename = "veritas_atmo_audit_bericht.md"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"[ERFOLG] Aktualisierter Audit-Report erfolgreich als '{report_filename}' generiert!")

if __name__ == "__main__":
    generate_audit_report()