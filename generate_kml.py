import json
import os

def generate_drone_mission():
    # 1. Vérification du rapport génétique (Étape 2)
    if not os.path.exists("rapport_diagnostic.json"):
        print("⚠️ Aucun rapport génétique trouvé. Exécutez d'abord le pipeline Étape 2.")
        return

    with open("rapport_diagnostic.json", "r") as f:
        diag_data = json.load(f)

    # Sécurité : Pas d'intervention si l'infection n'est pas confirmée
    if not diag_data.get("pathogen_confirmed", False):
        print("ℹ️ Diagnostic négatif : Aucune intervention drone nécessaire.")
        return

    lat = diag_data["gps_location"]["latitude"]
    lon = diag_data["gps_location"]["longitude"]
    radius_m = 15  # Rayon d'isolement du foyer

    # 2. Génération de la structure KML pour le contrôleur de vol (DJI / Pixhawk)
    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Mission Epandage Biocontrol - Parcelle BAN_08</name>
    <Placemark>
      <name>Foyer TR4 Validé ADN</name>
      <description>Diagnostic : Fusarium TR4 ({diag_data['infection_rate_percent']}% d'infection). Epandage ciblé sur rayon de {radius_m}m.</description>
      <Point>
        <coordinates>{lon},{lat},0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>"""

    # 3. Écriture du fichier KML
    with open("mission_drone.kml", "w", encoding="utf-8") as f:
        f.write(kml_content)

    print(f"✅ Mission KML générée avec succès : 'mission_drone.kml'")
    print(f"🛸 Cible d'épandage : [{lat} N, {lon} W] | Périmètre : {radius_m}m autour du point.")

if __name__ == "__main__":
    generate_drone_mission()