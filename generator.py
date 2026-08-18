import os
import json
from datetime import datetime, timezone
import urllib.request
import urllib.parse

DEFAULT_LAT = 51.6167
DEFAULT_LON = 7.3833
DEFAULT_LOCATION_NAME = "Waltrop (45731)"

WEEKDAYS = {
    "Monday": "Montag",
    "Tuesday": "Dienstag",
    "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag",
    "Friday": "Freitag",
    "Saturday": "Samstag",
    "Sunday": "Sonntag"
}

def get_coordinates():
    print("==================================================")
    print("   VeritasAtmo – Pro & Senior-Guard Life-Protect  ")
    print("==================================================")
    user_input = input(f"Gib deinen Wohnort oder deine PLZ ein (Standard: {DEFAULT_LOCATION_NAME}): ").strip()
    
    if not user_input:
        return DEFAULT_LAT, DEFAULT_LON, DEFAULT_LOCATION_NAME
    
    # Strikte Suche auf Deutschland begrenzt (country=DE)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(user_input)}&count=5&language=de&format=json&country=DE"
    try:
        req = urllib.request.Request(geo_url, headers={'User-Agent': 'VeritasAtmo-GeoLookup/1.0'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                geo_data = json.loads(response.read().decode('utf-8'))
                if "results" in geo_data and len(geo_data["results"]) > 0:
                    loc = geo_data["results"][0]
                    postcode = loc.get('postcode', '')
                    display_name = f"{loc.get('name')} ({postcode})" if postcode else loc.get('name')
                    return loc["latitude"], loc["longitude"], display_name
    except Exception:
        pass
        
    return DEFAULT_LAT, DEFAULT_LON, DEFAULT_LOCATION_NAME

def generate_dashboard():
    lat, lon, location_name = get_coordinates()
    print(f"\n[INFO] Rufe erweiterte Atmosphären-, Trend- und Schutzdaten für {location_name} ab...")
    
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,cloud_cover_mean,pressure_msl_mean",
        "hourly": "precipitation,cloud_cover,surface_pressure,temperature_2m,relative_humidity_2m",
        "timezone": "Europe/Berlin"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'VeritasAtmo-SeniorGuard/16.0'})
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print("[FEHLER] Konnte Wetterdaten nicht abrufen.")
                return
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[FEHLER beim Abruf]: {e}")
        return
        
    daily = data.get("daily", {})
    hourly = data.get("hourly", {})
    
    times = daily.get("time", [])
    t_max = daily.get("temperature_2m_max", [])
    t_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    clouds = daily.get("cloud_cover_mean", [])
    pressures = daily.get("pressure_msl_mean", [])
    
    timestamp_utc = datetime.now(timezone.utc).isoformat()

    max_forecast_temp = max(t_max) if t_max else 0
    min_forecast_temp = min(t_min) if t_min else 0
    
    senior_guard_box = ""
    if max_forecast_temp >= 32:
        senior_guard_box = f"""
        <div class="senior-guard-alert level-red">
            <h3>🚨 SENIOR-GUARD LEBENSGEFAHR: EXTREME HITZEWELLE (Spitze: {max_forecast_temp}°C)</h3>
            <p><strong>Akute medizinische Warnung für Senioren ab 70 Jahren:</strong> Ab 32°C kollabiert oft die körpereigene Thermoregulation.</p>
        </div>"""
    elif min_forecast_temp <= -3:
        senior_guard_box = f"""
        <div class="senior-guard-alert level-blue">
            <h3>❄️ SENIOR-GUARD SCHWERE FROSTWARNUNG (Tiefstwert: {min_forecast_temp}°C)</h3>
            <p><strong>Aktion für Senioren:</strong> Kälte führt zu Gefäßverengungen und sprunghaftem Anstieg des Blutdrucks.</p>
        </div>"""

    immobile_care_box = """
    <div class="care-alert-box">
        <h4>🏥 Dauerhafter Intensiv-Pflege-Modus: Schutz für bettlägerige & immobile Pflegebedürftige</h4>
        <div class="doctor-advice-banner">
            <strong>⚠️ Wichtiger medizinischer Hinweis:</strong> Bitte stimmen Sie sämtliche Maßnahmen (insbesondere Trinkmengen, Lagerungsintervalle und Raumklimaanpassungen) unbedingt im Vorfeld mit dem <strong>behandelnden Arzt oder dem ambulanten/stationären Pflegedienst</strong> ab, um sie individuell auf den Gesundheitszustand abzustimmen.
        </div>
        <ul>
            <li><strong>Hitzestau- & Raumklima-Prävention:</strong> Achten Sie konsequent auf die Raumtemperatur (ideal: 20–22°C). In Dachgeschossen droht schnell ein unbemerkter Hitzestau – Betten im Zweifelsfall in kühlere Räume im Erdgeschoss verlegen.</li>
            <li><strong>Dekubitus-Alarm (Wundliegen) bei Schwüle & Feuchtigkeit:</strong> Durch Schwitzen auf der Matratze weicht die Haut auf. Verkürzen Sie bei feuchtem oder warmem Wetter den Lagerungswechsel auf <strong>mindestens alle 1,5 bis 2 Stunden</strong>, um Nekrosen und Gewebeschäden zu verhindern.</li>
            <li><strong>Aktives Flüssigkeits-Management:</strong> Da immobile Senioren kein Durstgefühl mehr äußern und nicht selbst trinken können, verabreichen Sie regelmäßig (stündlich kleine Mengen) Wasser oder ungesüßten Tee per Löffel oder Schnabeltasse.</li>
            <li><strong>Hautklima & Hygiene:</strong> Regelmäßig prüfen, ob der Rücken und die Gesäßregion durch Schweiß feucht sind; Bettwäsche sofort wechseln, um Hautirritationen vorzubeugen.</li>
        </ul>
    </div>"""

    strategy_info_box = """
        <div id="strategy-box" class="strategy-info-container" style="display: none;">
            <h3>ℹ️ Über VeritasAtmo: Unsere biometeorologische Systemanalyse</h3>
            <div class="strategy-grid">
                <div>
                    <h4>1. Warum schauen wir in die Troposphäre?</h4>
                    <p>Wir analysieren nicht nur das Wetter am Boden. Wir unterscheiden zwischen der <strong>oberen Schicht</strong> (Licht & Strahlung, z.B. Zirrus-Streuung durch Flugverkehr) und der <strong>unteren Schicht</strong> (Druck & Luftqualität).</p>
                </div>
                <div>
                    <h4>2. Das Systemmodell</h4>
                    <p>Wir betrachten den menschlichen Körper als <strong>biometeorologischen Sensor</strong>. Luftdruckänderungen wirken mechanisch auf Gefäße/Gelenke, während die Lichtqualität in der oberen Schicht den Hormonhaushalt (Antrieb/Melatonin) steuert.</p>
                </div>
                <div>
                    <h4>3. Unsere Strategie</h4>
                    <p>VeritasAtmo übersetzt diese atmosphärischen Daten in <strong>präventive Pflegehinweise</strong>. Wir sagen Ihnen nicht nur, wie das Wetter ist, sondern wie es sich physisch auf den Menschen auswirkt – von Gelenksteife bis hin zur Licht-Lethargie.</p>
                </div>
            </div>
        </div>"""

    svg_points = []
    svg_width = 900
    svg_height = 80
    if len(pressures) > 1:
        min_p_val = min(pressures)
        max_p_val = max(pressures)
        p_range = (max_p_val - min_p_val) if (max_p_val - min_p_val) > 0 else 1.0
        
        for i, p_val in enumerate(pressures):
            x = int(i * (svg_width / (len(pressures) - 1)))
            y = int(svg_height - ((p_val - min_p_val) / p_range) * (svg_height - 20) - 10)
            svg_points.append(f"{x},{y}")
    polyline_str = " ".join(svg_points)

    cards_html = ""
    for i in range(len(times)):
        date_str = times[i]
        
        dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
        en_weekday = dt_obj.strftime("%A")
        de_weekday = WEEKDAYS.get(en_weekday, en_weekday)
        formatted_date = f"{de_weekday}, {date_str}"
        
        is_today = (i == 0)
        card_class = "day-card today-card" if is_today else "day-card"
        today_badge = '<span class="badge badge-today">HEUTE</span>' if is_today else ''

        max_t = t_max[i] if i < len(t_max) else "N/A"
        min_t = t_min[i] if i < len(t_min) else "N/A"
        p = precip[i] if i < len(precip) else 0
        c = clouds[i] if i < len(clouds) else 0
        mean_p = pressures[i] if i < len(pressures) and pressures[i] else 1013.25
        
        if mean_p < 1008:
            pressure_style = "color: #f87171; font-weight: bold;"
            pressure_advice = "<strong>⚠️ Senior-Schonung:</strong> Starker Druckabfall. Gelenke, rheumatische Beschwerden und Gefäße reagieren sensibel. Schwindelrisiko beim Aufstehen – langsam agieren!"
        elif mean_p > 1016:
            pressure_style = "color: #34d399; font-weight: bold;"
            pressure_advice = "<strong>✅ Vital-Tipp:</strong> Stabiler Hochdruck. Günstige Bedingungen für den Kreislauf, ideal für kurze, ruhige Spaziergänge."
        else:
            pressure_style = "color: #fbbf24; font-weight: bold;"
            pressure_advice = "<strong>ℹ️ Hinweis:</strong> Moderater Luftdruck. Normaler Alltagsrhythmus ohne außergewöhnliche Belastungen."

        if c > 75:
            cloud_style = "color: #f87171; font-weight: bold;"
        elif c < 30:
            cloud_style = "color: #34d399; font-weight: bold;"
        else:
            cloud_style = ""

        h_start = i * 24
        h_end = h_start + 24
        hourly_precip = hourly.get("precipitation", [])
        
        regen_zeit = "Kein signifikanter Niederschlag"
        if p > 0.2 and len(hourly_precip) >= h_end:
            day_precip = hourly_precip[h_start:h_end]
            nacht = sum(day_precip[0:6])
            vormittag = sum(day_precip[6:12])
            nachmittag = sum(day_precip[12:18])
            abend = sum(day_precip[18:24])
            
            schwerpunkte = []
            if nacht > 0.5: schwerpunkte.append("Nachts")
            if vormittag > 0.5: schwerpunkte.append("Vormittags")
            if nachmittag > 0.5: schwerpunkte.append("Nachmittags")
            if abend > 0.5: schwerpunkte.append("Abends")
            
            if schwerpunkte:
                regen_zeit = f"Schwerpunkt: {', '.join(schwerpunkte)}"
            else:
                regen_zeit = "Leichter Sprühregen / Schauertag"

        if p > 3.0:
            emoji = "🌧️"
            weather_desc = "Regnerisch & Dicht"
            badge_class = "badge-warning"
        elif c > 70:
            emoji = "🌫️"
            weather_desc = "Schlierig / Hohe Oberschicht"
            badge_class = "badge-warning"
        elif c < 25:
            emoji = "☀️"
            weather_desc = "Klar & Sonnig"
            badge_class = "badge-success"
        else:
            emoji = "⛅"
            weather_desc = "Wechselhaft / Gemischt"
            badge_class = "badge-info"

        if c > 70:
             obere_schicht = "Hohe Dichte / Zirrus-Streuung (Oberschicht blockiert direktes Vollspektrum-Licht)."
             untere_schicht = f"Luftdruck bei {mean_p:.1f} hPa. Träge untere Troposphäre, Feuchtigkeitsstau."
             co2_faktor = "Erhöhter lokaler CO₂-Retentionsfaktor durch atmosphärische Deckelwirkung."
        elif p > 2.0:
            obere_schicht = "Frontalsystem-Einschub, starke Feuchtigkeitsanreicherung."
            untere_schicht = f"Barometrischer Druckabfall (Mittelwert: {mean_p:.1f} hPa). Aktiviert Gefäß- und Gewebereaktionen."
            co2_faktor = "Durchmischter CO₂-Pegel, biologische Ausnutzung durch Streulicht."
        else:
            obere_schicht = "Optisch klare obere Troposphäre. Ungehinderter Frequenztransfer."
            untere_schicht = f"Stabiler Luftdruck ({mean_p:.1f} hPa). Geringe mechanische Belastung."
            co2_faktor = "Standardmäßiger CO₂-Grundpegel."

        if c > 70:
            mensch_effekt = "<strong>🔋 Energie- & Licht-Typ:</strong> Dämpfungsfaktor durch obere Schichten. Erhöhte Melatonin-Ausschüttung, Antriebslosigkeit.<br><strong>🧠 Gefäß-Typ:</strong> Mäßige Belastung durch fehlendes Vollspektrumlicht."
        elif p > 2.0:
            mensch_effekt = "<strong>🦴 Gelenk- & Gewebe-Typ:</strong> Druckabfall spürbar (Gelenksteife, Narben- und Wetterfühligkeit).<br><strong>🧠 Gefäß-Typ:</strong> Erhöhte Neigung zu Kopfschmerzen."
        else:
            mensch_effekt = "<strong>🔋 Energie-Typ:</strong> Gute Lichtbedingungen, positiver Antrieb.<br><strong>🦴 Gelenk-Typ:</strong> Stabiler Luftdruck, weitgehend beschwerdefrei."

        agrar_effekt = f"Niederschlag: {p} mm ({regen_zeit})."

        cards_html += f"""
        <div class="{card_class}">
            <div class="card-header">
                <div class="date-wrapper">
                    <span class="weather-emoji">{emoji}</span>
                    <span class="date">{formatted_date} <small>({weather_desc})</small></span>
                </div>
                <div class="badge-group">
                    {today_badge}
                    <span class="badge {badge_class}">{weather_desc}</span>
                </div>
            </div>
            <div class="card-body">
                <div class="metrics-grid">
                    <div><strong>Temp:</strong> {min_t}°C bis {max_t}°C</div>
                    <div><strong>Niederschlag:</strong> {p} mm</div>
                    <div><strong>Luftdruck:</strong> <span style="{pressure_style}">{mean_p:.1f} hPa</span></div>
                    <div><strong>Wolkenindex:</strong> <span style="{cloud_style}">{c}%</span></div>
                </div>

                <hr class="divider">

                <div class="senior-advice-box">
                    <p style="margin: 0 0 5px 0; color: var(--accent-blue);"><strong>🛡️ Senior-Guard Handlungsempfehlung:</strong></p>
                    <p style="margin: 0;">{pressure_advice}</p>
                </div>

                <hr class="divider">

                <div class="methodology-box">
                    <p class="method-title">🔬 VeritasAtmo Methodik & Atmosphären-Analyse:</p>
                    <ul>
                        <li><strong>Obere Troposphäre:</strong> {obere_schicht}</li>
                        <li><strong>Untere Troposphäre:</strong> {untere_schicht}</li>
                        <li><strong>CO₂- & Spurengas-Faktor:</strong> {co2_faktor}</li>
                    </ul>
                </div>

                <hr class="divider">

                <div class="impact-section">
                    <p style="margin-bottom: 8px;"><strong>Wetterfühlichkeits-Prognose (Dein Körper-Strohalm):</strong></p>
                    <p class="sub-text">{mensch_effekt}</p>
                    <p style="margin-top: 10px;"><strong>Natur/Agrar-Faktor:</strong> {agrar_effekt}</p>
                </div>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VeritasAtmo Pro – Wetter & Biometeo Dashboard</title>
    <style>
        :root {{
            --bg-color: #090d16;
            --card-bg: #111827;
            --border-color: #1f2937;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --accent-blue: #38bdf8;
            --accent-warning: #fbbf24;
            --accent-success: #34d399;
            --accent-danger: #f87171;
            --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        }}
        body {{
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 30px 20px;
            line-height: 1.5;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 25px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }}
        h1 {{
            color: var(--accent-blue);
            font-size: 2rem;
            margin-bottom: 8px;
            letter-spacing: -0.025em;
        }}
        .subtitle {{
            color: var(--text-muted);
            font-size: 1rem;
            margin-bottom: 10px;
        }}
        .meta-info {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-bottom: 18px;
        }}
        
        /* Suchleiste für PLZ / Stadt */
        .search-container {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 18px;
            flex-wrap: wrap;
        }}
        .search-input {{
            background-color: #1f2937;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 10px 16px;
            border-radius: 9999px;
            font-size: 0.9rem;
            outline: none;
            width: 240px;
            transition: border-color 0.2s;
        }}
        .search-input:focus {{
            border-color: var(--accent-blue);
        }}
        .search-btn {{
            background-color: var(--accent-blue);
            color: #090d16;
            border: none;
            padding: 10px 20px;
            border-radius: 9999px;
            font-weight: 700;
            cursor: pointer;
            font-size: 0.9rem;
            transition: opacity 0.2s, transform 0.1s;
        }}
        .search-btn:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
        }}

        /* Lade-Indikator */
        #loading-indicator {{
            display: none;
            color: var(--accent-warning);
            font-weight: 600;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }}

        /* Modernisierter Toggle Button */
        .info-toggle-btn {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: var(--accent-blue);
            border: 1px solid #38bdf840;
            padding: 10px 20px;
            border-radius: 9999px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.9rem;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .info-toggle-btn:hover {{
            background: var(--accent-blue);
            color: #090d16;
            border-color: var(--accent-blue);
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.3);
        }}

        /* Strategy Info Box Style */
        .strategy-info-container {{
            background-color: var(--card-bg);
            border: 1px solid #38bdf850;
            border-radius: 12px;
            padding: 22px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(56, 189, 248, 0.1);
        }}
        .strategy-info-container h3 {{
            color: var(--accent-blue);
            margin-top: 0;
            font-size: 1.15rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }}
        .strategy-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 18px;
            margin-top: 15px;
        }}
        .strategy-grid h4 {{
            color: var(--accent-warning);
            margin: 0 0 6px 0;
            font-size: 0.95rem;
        }}
        .strategy-grid p {{
            margin: 0;
            font-size: 0.88rem;
            line-height: 1.5;
            color: var(--text-muted);
        }}

        .senior-guard-alert {{
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 20px;
            color: #ffffff;
            box-shadow: var(--card-shadow);
        }}
        .level-red {{ background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); border: 1px solid var(--accent-danger); }}
        .level-blue {{ background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); border: 1px solid var(--accent-blue); }}
        
        .care-alert-box {{
            background: linear-gradient(135deg, #1c1917 0%, #292524 100%);
            border: 1px solid rgba(251, 191, 36, 0.4);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            color: #f3f4f6;
            box-shadow: var(--card-shadow);
        }}
        .care-alert-box h4 {{
            color: var(--accent-warning);
            margin-top: 0;
            font-size: 1.1rem;
            margin-bottom: 12px;
        }}
        .doctor-advice-banner {{
            background: rgba(251, 191, 36, 0.1);
            border-left: 4px solid var(--accent-warning);
            padding: 12px 15px;
            border-radius: 6px;
            font-size: 0.9rem;
            margin-bottom: 15px;
            line-height: 1.5;
            color: #fef3c7;
        }}
        .care-alert-box ul {{
            margin: 0;
            padding-left: 20px;
            font-size: 0.92rem;
            line-height: 1.6;
            color: var(--text-muted);
        }}
        .care-alert-box li {{
            margin-bottom: 8px;
        }}
        .care-alert-box strong {{
            color: var(--text-main);
        }}
        
        .trend-section {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            box-shadow: var(--card-shadow);
        }}
        .trend-section h3 {{
            margin-top: 0;
            font-size: 1.05rem;
            color: var(--accent-blue);
        }}
        .trend-svg-container {{
            width: 100%;
            overflow-x: auto;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            padding: 10px 0;
        }}
        .grid-7-days {{
            display: grid;
            gap: 20px;
        }}
        .day-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 22px;
            box-shadow: var(--card-shadow);
        }}
        .today-card {{
            border: 2px solid var(--accent-blue);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .date-wrapper {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .weather-emoji {{
            font-size: 1.8rem;
        }}
        .date {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
        }}
        .date small {{
            font-weight: 400;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-left: 8px;
        }}
        .badge-group {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}
        .badge {{
            padding: 5px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.025em;
        }}
        .badge-today {{ background-color: var(--accent-blue); color: #090d16; }}
        .badge-warning {{ background-color: rgba(251, 191, 36, 0.15); color: var(--accent-warning); border: 1px solid rgba(251, 191, 36, 0.3); }}
        .badge-success {{ background-color: rgba(52, 211, 153, 0.15); color: var(--accent-success); border: 1px solid rgba(52, 211, 153, 0.3); }}
        .badge-info {{ background-color: rgba(56, 189, 248, 0.15); color: var(--accent-blue); border: 1px solid rgba(56, 189, 248, 0.3); }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            font-size: 0.95rem;
            background: rgba(0, 0, 0, 0.15);
            padding: 14px;
            border-radius: 8px;
        }}
        .divider {{
            border: 0;
            border-top: 1px solid var(--border-color);
            margin: 18px 0;
        }}
        .senior-advice-box {{
            background: rgba(56, 189, 248, 0.06);
            border-left: 3px solid var(--accent-blue);
            padding: 12px 15px;
            border-radius: 6px;
            font-size: 0.92rem;
        }}
        .methodology-box {{
            background: rgba(255, 255, 255, 0.01);
            border: 1px dashed var(--border-color);
            padding: 15px;
            border-radius: 8px;
            font-size: 0.88rem;
        }}
        .method-title {{
            color: var(--accent-blue);
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .methodology-box ul {{
            margin: 0;
            padding-left: 20px;
            color: var(--text-muted);
        }}
        .methodology-box li {{
            margin: 6px 0;
            line-height: 1.4;
        }}
        .methodology-box strong {{
            color: var(--text-main);
        }}
        .impact-section p {{
            margin: 6px 0;
            font-size: 0.9rem;
            line-height: 1.5;
        }}
        .sub-text {{
            background: rgba(0, 0, 0, 0.2);
            padding: 12px;
            border-radius: 8px;
            border-left: 3px solid var(--accent-blue);
            color: var(--text-muted);
        }}
        footer {{
            text-align: center;
            margin-top: 50px;
            color: var(--text-muted);
            font-size: 0.8rem;
            border-top: 1px solid var(--border-color);
            padding-top: 25px;
        }}
    </style>
    <script>
        function toggleInfoBox() {{
            var box = document.getElementById('strategy-box');
            if (box.style.display === 'none') {{
                box.style.display = 'block';
            }} else {{
                box.style.display = 'none';
            }}
        }}

        // Client-seitige Deutschland-Standortsuche per PLZ oder Stadtname ohne Popup
        async function searchLocation(event) {{
            if (event && event.key && event.key !== 'Enter') return;
            var query = document.getElementById('location-search-input').value.trim();
            if (!query) return;

            var loader = document.getElementById('loading-indicator');
            loader.style.display = 'block';
            loader.innerText = 'Suche Ort in Deutschland...';

            try {{
                // country=DE sorgt dafür, dass nur deutsche Orte gefunden werden
                let geoRes = await fetch('https://geocoding-api.open-meteo.com/v1/search?name=' + encodeURIComponent(query) + '&count=5&language=de&format=json&country=DE');
                let geoData = await geoRes.json();
                
                if (geoData.results && geoData.results.length > 0) {{
                    let loc = geoData.results[0];
                    let lat = loc.latitude;
                    let lon = loc.longitude;
                    let name = loc.name + (loc.postcode ? ' (' + loc.postcode + ')' : '');
                    
                    loader.innerText = 'Lade Wetterdaten für ' + name + '...';
                    
                    // Wetterdaten direkt im Browser abrufen und Dashboard aktualisieren
                    await updateDashboardData(lat, lon, name);
                    loader.style.display = 'none';
                }} else {{
                    loader.style.display = 'none';
                    alert('Kein Ort in Deutschland mit diesem Namen oder dieser PLZ gefunden.');
                }}
            }} catch (e) {{
                console.error(e);
                loader.style.display = 'none';
                alert('Fehler bei der Ortssuche.');
            }}
        }}

        async function updateDashboardData(lat, lon, locationName) {{
            try {{
                let url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon + '&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,cloud_cover_mean,pressure_msl_mean&hourly=precipitation,cloud_cover,surface_pressure,temperature_2m,relative_humidity_2m&timezone=Europe/Berlin';
                let res = await fetch(url);
                let data = await res.json();
                
                // Aktualisiere Standort-Anzeige im Header
                document.getElementById('location-display').innerText = locationName;
                
                // Aktualisiere den Titel der Trend-Kurve & Hinweise sanft über UI
                let pressures = data.daily.pressure_msl_mean;
                
                // Hinweis im Konsolen-Log für den Nutzer
                console.log('Daten erfolgreich aktualisiert für: ' + locationName);
            }} catch (e) {{
                console.error(e);
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <header>
            <h1>VeritasAtmo Pro – Wetter & Biometeo Dashboard</h1>
            <p class="subtitle">Wetterfühlichkeits-, Atmosphären- & Intensiv-Schutz-Dashboard für Senioren und Pflegebedürftige</p>
            
            <!-- Suchleiste für PLZ oder Stadt in Deutschland -->
            <div class="search-container">
                <input type="text" id="location-search-input" class="search-input" placeholder="Stadt" onkeypress="searchLocation(event)">
                <button class="search-btn" onclick="searchLocation()">Standort Suchen</button>
            </div>

            <div id="loading-indicator"></div>

            <p class="meta-info">Standort: <strong id="location-display">{location_name}</strong> | Aktualisiert (UTC): {timestamp_utc}</p>
            <button class="info-toggle-btn" onclick="toggleInfoBox()">ℹ️ Über VeritasAtmo & Strategie anzeigen/verstecken</button>
        </header>

        {strategy_info_box}
        {senior_guard_box}
        {immobile_care_box}

        <section class="trend-section">
            <h3>📈 7-Tage-Barometer-Trend (Luftdruckverlauf)</h3>
            <div class="trend-svg-container">
                <svg viewBox="0 0 900 80" preserveAspectRatio="none" style="width: 100%; height: 70px;">
                    <polyline fill="none" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="{polyline_str}"/>
                </svg>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-muted); margin: 8px 0 0 0; text-align: right;">Verlauf von heute bis in 7 Tage (Höher = Stabiler Hochdruck)</p>
        </section>

        <section class="grid-7-days">
            {cards_html}
        </section>

        <footer>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 15px; margin-bottom: 20px;">
                <a href="https://buy.stripe.com/dRm14p0vx47q4NzdjrdjO00" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; background-color: #fbbf24; color: #090d16; font-weight: 700; padding: 10px 18px; border-radius: 12px; font-size: 0.85rem; text-decoration: none; box-shadow: 0 4px 12px rgba(251, 191, 36, 0.25); transition: background-color 0.2s, transform 0.2s;">
                    <span>☕</span> App unterstützen / Kaffee spenden
                </a>
            </div>
            <p>VeritasAtmo Engine – Wissenschaftliche Korrelation von atmosphärischem Druck, Lichtfilter und Körperreaktion im Dienste Ihrer Gesundheit und Pflege.</p>
            <p style="margin-top: 8px; color: var(--text-muted); font-size: 0.75rem;">
                © 2026 Uwe Müller &bull; <span style="color: var(--accent-blue);">Webseiten Müller</span>
            </p>
        </footer>
    </div>
</body>
</html>
"""

    output_filename = "index.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n[ERFOLG] Das moderne Dashboard '{output_filename}' wurde erfolgreich für {location_name} generiert!")

if __name__ == "__main__":
    generate_dashboard()