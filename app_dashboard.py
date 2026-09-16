import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Chargement des données du Bloc 3
json_path = "rapport_diagnostic.json"
if not os.path.exists(json_path):
    print("[ERREUR] Fichier 'rapport_diagnostic.json' introuvable. Exécutez d'abord run_align_pure.py")
    exit()

with open(json_path, "r", encoding="utf-8") as f:
    diag_data = json.load(f)

# 2. Simulation des données IoT et Spatiales (Bloc 4)
iot_data = {
    "parcelle": "Parcelle BAN_07",
    "humidite_sol": "72%",
    "temperature": "28 °C",
    "pluie_24h": "4 mm",
    "statut": "Infection Détectée",
    "recommandation": "Pulvérisation ciblée de biocontrôle (-85% pesticides)"
}

# 3. Création du Tableau de Bord Interactif (Bloc 5)
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Carte d'Infection (Heatmap Parcelle BAN_07)",
        "Répartition des Reads Analysés",
        "Historique de Température & Humidité",
        "Diagnostic & Action Agronomique"
    ),
    specs=[[{"type": "mapbox"}, {"type": "pie"}],
           [{"type": "xy"}, {"type": "indicator"}]]
)

# Graphique 1 : Carte d'Infection (Heatmap)
fig.add_trace(
    go.Scattermapbox(
        lat=[30.420, 30.422, 30.425, 30.421, 30.424],
        lon=[-9.598, -9.595, -9.592, -9.590, -9.596],
        mode='markers',
        marker=dict(
            size=[15, 35, 12, 10, 40],
            color=['green', 'red', 'yellow', 'green', 'red'],
            opacity=0.8
        ),
        text=["Zone Saine", "Foyer Infecté (TR4)", "Zone Suspecte", "Zone Saine", "Foyer Infecté (TR4)"]
    ),
    row=1, col=1
)

# Graphique 2 : Camembert d'Alignement
aligned = diag_data.get("aligned_reads", 0)
total = diag_data.get("total_reads", 1)
non_aligned = total - aligned

fig.add_trace(
    go.Pie(
        labels=["Fusarium TR4", "Autres / Hôte"],
        values=[aligned, non_aligned],
        marker_colors=["#e74c3c", "#2ecc71"],
        hole=0.4
    ),
    row=1, col=2
)

# Graphique 3 : Courbes Capteurs IoT
fig.add_trace(
    go.Scatter(x=["15/05", "16/05", "17/05", "18/05", "19/05", "20/05"], y=[24, 25, 27, 28, 28, 29], name="Température (°C)", line=dict(color="orange")),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=["15/05", "16/05", "17/05", "18/05", "19/05", "20/05"], y=[65, 68, 70, 72, 71, 72], name="Humidité Sol (%)", line=dict(color="blue")),
    row=2, col=1
)

# Graphique 4 : Indicateur Taux d'Infection
fig.add_trace(
    go.Indicator(
        mode="number+delta",
        value=diag_data.get("infection_rate", 0),
        number={'suffix': "%"},
        title={"text": f"Espèce : Fusarium oxysporum TR4<br><span style='font-size:0.8em;color:gray'>{iot_data['recommandation']}</span>"},
        domain={'x': [0.5, 1], 'y': [0, 0.5]}
    ),
    row=2, col=2
)

# Configuration de la carte Mapbox
fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=30.422, lon=-9.594),
        zoom=14
    ),
    title_text=f"AgriSeq Edge — Tableau de Bord Diagnostic [{iot_data['parcelle']}]",
    showlegend=False,
    height=800
)

# Sauvegarde sous forme de page HTML interactive
output_html = "dashboard_agriseq.html"
fig.write_html(output_html)
print(f"-> Tableau de bord généré avec succès : '{output_html}'")
