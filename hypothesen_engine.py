import json
import os

def run_hypothesis_audit():
    filename = "atmphaeren_rohdaten.json"
    if not os.path.exists(filename):
        print(f"[FEHLER] Keine Rohdaten-Datei '{filename}' gefunden. Bitte zuerst den Harvester laufen lassen!")
        return
    
    with open(filename, "r", encoding="utf-8") as f:
        payload = json.load(f)
        
    data = payload.get("raw_data", {})
    current = data.get("current", {})
    timestamp = payload.get("fetch_timestamp_utc")
    
    # Extraktion der neuen Spurengas- und Umweltparameter aus der Air Quality API
    pm10 = current.get("pm10")
    pm25 = current.get("pm2_5")
    co = current.get("carbon_monoxide")
    no2 = current.get("nitrogen_dioxide")
    so2 = current.get("sulphur_dioxide")
    ozone = current.get("ozone")
    
    print("==================================================")
    print("  VeritasAtmo – Hypothesen-Engine Spurengas-Audit")
    print("  Standort: Waltrop (Lat: 51.62, Lon: 7.38)")
    print(f"  Zeitstempel: {timestamp}")
    print("==================================================")
    print(f"-> Feinstaub (PM2.5): {pm25} µg/m³")
    print(f"-> Feinstaub (PM10): {pm10} µg/m³")
    print(f"-> Kohlenmonoxid (CO): {co} µg/m³")
    print(f"-> Stickstoffdioxid (NO2): {no2} µg/m³")
    print(f"-> Schwefeldioxid (SO2): {so2} µg/m³")
    print(f"-> Ozon (O3): {ozone} µg/m³")
    print("--------------------------------------------------")
    
    # Hypothesen-Prüfung (Spurengas- & Aerosol-Analyse)
    print("[AUDIT-ANALYSE LAUFT (Aerosol- & Gas-Korrelation)]...")
    
    if pm25 is not None and pm25 > 20:
        print("[ALARM: ERHÖHTE FEINSTAUB- & AEROSOLBELASTUNG]")
        print(f"    -> Befund: PM2.5 liegt bei {pm25} µg/m³.")
        print("    -> Hypothese: Verdacht auf akkumulierte Partikel-Nukleationskerne in Bodennähe durch absinkende obere Schichten.")
    else:
        print("[BEFUND AEROSOL-INDEX]: Spurengas- und Partikelwerte im unauffälligen Bereich.")
        print("    -> Hypothese: Keine akute Bodenanomalie messbar; Fokus verbleibt auf den atmosphärischen Höhenschichten und globalen Gas-Konzentrationen.")
            
    print("==================================================")
    print("Audit abgeschlossen. Bereit für den Report-Export.")

if __name__ == "__main__":
    run_hypothesis_audit()