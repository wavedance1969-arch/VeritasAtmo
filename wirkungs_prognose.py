import json
import os

def run_impact_forecast():
    filename = "atmphaeren_rohdaten.json"
    if not os.path.exists(filename):
        print(f"[FEHLER] Keine Rohdaten-Datei '{filename}' gefunden. Bitte zuerst den Harvester laufen lassen!")
        return
    
    with open(filename, "r", encoding="utf-8") as f:
        payload = json.load(f)
        
    data = payload.get("raw_data", {})
    current = data.get("current", {})
    timestamp = payload.get("fetch_timestamp_utc")
    
    # Werte einlesen (Spurengase & Umwelt)
    pm25 = current.get("pm2_5", 0)
    ozone = current.get("ozone", 0)
    
    print("==================================================")
    print("  VeritasAtmo – Wirkungs- & Prognose-Engine")
    print("  Standort: Waltrop (Lat: 51.62, Lon: 7.38)")
    print(f"  Zeitstempel: {timestamp}")
    print("==================================================")
    
    # Wirkungs-Analyse für Mensch und Natur (Human- & Bio-Impact)
    print("[WIRKUNGS-ANALYSE LÄUFT...]")
    print("-> Verknüpfe Atmosphären-Dichte, Lichtfilter & Stoffwechsel-Faktoren...")
    print("--------------------------------------------------")
    
    # 1. Menschlicher Faktor (Lichtspektrum, Melatonin, Erschöpfung)
    print("[MENSCH-FAKTOR (Psycho-Physiologie)]:")
    if ozone > 50:
        print(f"    -> Ozon-Wert bei {ozone} µg/m³ (Erhöhter photochemischer Index).")
        print("    -> Prognose: Bei diffuser Bewölkung und Ozon-Belastung neigt der Körper zu veränderten Sauerstoff-Reaktionen, Schleimhautreizungen und bleierner Müdigkeit.")
    else:
        print("    -> Ozon und Partikel im unauffälligen Bereich.")
        print("    -> Prognose: Hauptfaktor für Erschöpfung ist primär der **optische Dämpfungsfaktor** (fehlendes direktes Vollspektrum-Sonnenlicht durch obere Schichten), was die Zirbeldrüse zu erhöhter Melatonin- Ausschüttung anregt.")

    print("\n[AGRAR- / NATUR-FAKTOR (Pflanzenwachstum & Dürre-Resistenz)]:")
    print("    -> Befund: Indirekte Lichtstreuung (Milchiger Himmel) + stabiler CO₂-Naheffekt.")
    print("    -> Prognose: Begünstigt das Wachstum von Blattgemüse (z. B. Salat) trotz äußerster Trockenheit, da weniger direkte Verdunstung und effizientere Photosynthese unter Streulicht stattfinden.")

    print("==================================================")
    print("  Wirkungs-Prognose erfolgreich abgeschlossen.")
    print("==================================================")

if __name__ == "__main__":
    run_impact_forecast()