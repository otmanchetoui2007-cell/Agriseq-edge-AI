import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURATION DE LA PAGE
# ---------------------------------------------------------
st.set_page_config(
    page_title="AgriSeq Edge 3D - TR4",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS pour assurer le thème sombre et la lisibilité
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stMetric { background-color: #1E222D; padding: 15px; border-radius: 8px; border: 1px solid #2E3A4E; }
    .card-info { background-color: #132338; border-left: 4px solid #00E5FF; padding: 15px; border-radius: 6px; margin-bottom: 10px; }
    .card-alert { background-color: #381A1A; border-left: 4px solid #FF4B4B; padding: 15px; border-radius: 6px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Coordonnées du foyer d'infection (Gharb, Maroc)
LAT_TARGET, LON_TARGET = 34.3122, -6.3548

# ---------------------------------------------------------
# EN-TÊTE
# ---------------------------------------------------------
st.title("🌾 Plateforme AgTech 3D : Détection & Intervention TR4")
st.caption("Exploitation active : **Domaine Agricole du Gharb — Parcelle BAN_08** | Cible : *Fusarium oxysporum TR4*")

tab1, tab2, tab3 = st.tabs([
    "🛰️ Étape 1 : Détection Satellite 3D (NDVI)",
    "🧬 Étape 2 : Validation ADN 3D (Nanopore)",
    "🛸 Étape 3 : Intervention Drone 3D (Plan de Vol)"
])

# =========================================================
# ÉTAPE 1 : CARTE SATELLITE & STRESS NDVI 3D
# =========================================================
with tab1:
    st.subheader("🛰️ Étape 1 : Cartographie du Stress Végétal en 3D (NDVI)")
    st.write("Analyse spatiale de la vigueur végétale. Les colonnes rouges représentent les zones à fort stress phytosanitaire.")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Génération d'une grille de points NDVI autour de la cible
        np.random.seed(42)
        lats = LAT_TARGET + np.random.uniform(-0.003, 0.003, 80)
        lons = LON_TARGET + np.random.uniform(-0.003, 0.003, 80)
        
        # Calcul de la distance au foyer pour simuler la baisse NDVI
        dists = np.sqrt((lats - LAT_TARGET)**2 + (lons - LON_TARGET)**2)
        ndvi_vals = np.clip(0.8 - (0.6 / (dists * 1000 + 1)), 0.15, 0.85)
        heights = (1 - ndvi_vals) * 300  # Plus le NDVI est bas, plus la colonne 3D est haute

        df_ndvi = pd.DataFrame({
            'lat': lats,
            'lon': lons,
            'ndvi': ndvi_vals,
            'height': heights,
            'r': (1 - ndvi_vals) * 255,
            'g': ndvi_vals * 255,
            'b': 50
        })

        # PyDeck ColumnLayer 3D
        layer_3d_ndvi = pdk.Layer(
            "ColumnLayer",
            df_ndvi,
            get_position=["lon", "lat"],
            get_elevation="height",
            elevation_scale=1,
            radius=8,
            get_fill_color=["r", "g", "b", 200],
            pickable=True,
            auto_highlight=True
        )

        view_state_1 = pdk.ViewState(
            latitude=LAT_TARGET,
            longitude=LON_TARGET,
            zoom=16.5,
            pitch=55,
            bearing=-20
        )

        st.pydeck_chart(pdk.Deck(
            layers=[layer_3d_ndvi],
            initial_view_state=view_state_1,
            map_style="mapbox://styles/mapbox/satellite-v9",
            tooltip={"text": "NDVI : {ndvi}\nHauteur Stress : {height}m"}
        ))

    with col2:
        st.markdown(f"""
        <div class="card-info">
            <h4>📍 Coordonnées GPS de l'Anomalie</h4>
            <ul>
                <li><b>Latitude :</b> {LAT_TARGET:.4f} N</li>
                <li><b>Longitude :</b> {LON_TARGET:.4f} W</li>
                <li><b>Indice NDVI Moyen :</b> <span style="color:#FF4B4B;">0.32 (Baisse Critique)</span></li>
                <li><b>Surface impactée estimée :</b> 250 m²</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-alert">
            ⚠️ <b>Action Recommandée :</b><br>
            La baisse de vigueur végétale ne prouve pas à elle seule la présence du champignon <i>Fusarium TR4</i>.<br><br>
            👉 Depêcher un technicien aux coordonnées GPS ci-dessus pour prélever un échantillon de racine et passer à l'<b>Étape 2</b>.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# ÉTAPE 2 : MOLECULAIRE & DNA BASECALLING 3D
# =========================================================
with tab2:
    st.subheader("🧬 Étape 2 : Confirmation Microbiologique par Séquençage ADN (Modèle 3D)")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Reads Total (Émulé)", "70,244")
    m2.metric("Reads Alignés (TR4)", "7,792")
    m3.metric("Taux d'Infection Cible", "11.10%", delta="Alerte Pathogène", delta_color="inverse")
    m4.metric("Score de Confiance IA", "97.3%")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("**Structure 3D de la Double Hélice d'ADN en Translocation**")
        
        # Génération d'une double hélice ADN en 3D avec Plotly
        t = np.linspace(0, 4 * np.pi, 120)
        z = t * 2
        x1, y1 = np.sin(t), np.cos(t)
        x2, y2 = np.sin(t + np.pi), np.cos(t + np.pi)

        fig_dna = go.Figure()

        # Brin 1
        fig_dna.add_trace(go.Scatter3d(x=x1, y=y1, z=z, mode='markers+lines',
                                     marker=dict(size=5, color='#00E5FF'),
                                     line=dict(color='#00E5FF', width=4), name="Brin Sens (5'-3')"))
        # Brin 2
        fig_dna.add_trace(go.Scatter3d(x=x2, y=y2, z=z, mode='markers+lines',
                                     marker=dict(size=5, color='#FF4B4B'),
                                     line=dict(color='#FF4B4B', width=4), name="Brin Anti-sens"))

        # Liaisons hydrogène
        for i in range(0, len(t), 4):
            fig_dna.add_trace(go.Scatter3d(x=[x1[i], x2[i]], y=[y1[i], y2[i]], z=[z[i], z[i]],
                                         mode='lines', line=dict(color='#FFFFFF', width=2), showlegend=False))

        fig_dna.update_layout(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                bgcolor='#0E1117'
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='#0E1117',
            height=380
        )
        st.plotly_chart(fig_dna, use_container_width=True)

    with col_b:
        st.markdown("**Console Séquenceur Nanopore (Flux Live)**")
        st.code("""
>read_nanopore_01_tr4_pos | LEN: 173 bp | Q: 17.22
AACGCACACTCACACTCACACACTCACACTCACACACGAATTATACCACACACAGATTTATATCG

[MATCH CONFIRMÉ] Alignement à 99.8% sur gène ITS Fusarium TR4 (NCBI AY520188.1)
        """, language="text")

        # Camembert répartition
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Musa acuminata (Hôte)', 'Autres Microbes', 'Fusarium oxysporum TR4'],
            values=[68.5, 20.4, 11.1],
            hole=.4,
            marker_colors=['#FF4B4B', '#00E676', '#2979FF']
        )])
        fig_pie.update_layout(
            paper_bgcolor='#0E1117',
            font_color='#FFFFFF',
            margin=dict(l=20, r=20, t=20, b=20),
            height=250
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# =========================================================
# ÉTAPE 3 : DRONE 3D & PLAN DE VOL KML
# =========================================================
with tab3:
    st.subheader("🛸 Étape 3 : Plan de Vol 3D & Traitement Ciblé par Drone")

    col_drone_left, col_drone_right = st.columns([2, 1])

    # Fonction de génération de fichier KML
    def generate_kml(lat, lon):
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Mission_Drone_TR4_Gharb</name>
    <Placemark>
      <name>Foyer Infection TR4</name>
      <Point><coordinates>{lon},{lat},0</coordinates></Point>
    </Placemark>
  </Document>
</kml>"""

    with col_drone_left:
        st.markdown("**Simulateur de Trajectoire de Vol Drone 3D (Altitude: 12m)**")

        # Création d'une trajectoire de vol 3D en spirale au-dessus du foyer
        angles = np.linspace(0, 6 * np.pi, 50)
        radii = np.linspace(0.0001, 0.0008, 50)
        path_lats = LAT_TARGET + radii * np.sin(angles)
        path_lons = LON_TARGET + radii * np.cos(angles)
        
        path_coordinates = [[lon, lat, 12] for lat, lon in zip(path_lats, path_lons)]
        # Ajout décollage / atterrissage
        full_path = [[LON_TARGET - 0.001, LAT_TARGET - 0.001, 0], [LON_TARGET - 0.001, LAT_TARGET - 0.001, 12]] + path_coordinates

        # PyDeck PathLayer 3D
        drone_path_layer = pdk.Layer(
            "PathLayer",
            [{"path": full_path}],
            get_path="path",
            get_color=[0, 229, 255, 255],
            width_min_pixels=4
        )

        # Cylindre 3D représentant la zone d'épandage de 15m
        spray_zone_layer = pdk.Layer(
            "ColumnLayer",
            pd.DataFrame([{'lat': LAT_TARGET, 'lon': LON_TARGET}]),
            get_position=["lon", "lat"],
            get_elevation=15,
            radius=15,
            get_fill_color=[255, 75, 75, 100],
            pickable=True
        )

        view_state_3d = pdk.ViewState(
            latitude=LAT_TARGET,
            longitude=LON_TARGET,
            zoom=17.5,
            pitch=60,
            bearing=30
        )

        st.pydeck_chart(pdk.Deck(
            layers=[spray_zone_layer, drone_path_layer],
            initial_view_state=view_state_3d,
            map_style="mapbox://styles/mapbox/satellite-v9"
        ))

    with col_drone_right:
        st.markdown("""
        <div class="card-alert" style="background-color: #241616;">
            <h4>🚨 ORDRE DE TRAITEMENT LOCALISÉ</h4>
            <ul>
                <li><b>Zone d'épandage :</b> Rayon strict de 15 mètres autour du point [{lat:.4f}, {lon:.4f}].</li>
                <li><b>Produit prescrit :</b> Agent de biocontrôle (<i>Pseudomonas protegens</i>) ou bio-fongicide homologué.</li>
                <li><b>Économie estimée :</b> <span style="color:#00E676;">92% de produit phytosanitaire économisé</span> par rapport à un traitement global.</li>
                <li><b>Consigne Biosécurité :</b> Isoler les serres adjacentes et désinfecter les outils de coupe.</li>
            </ul>
        </div>
        """.format(lat=LAT_TARGET, lon=LON_TARGET), unsafe_allow_html=True)

        kml_data = generate_kml(LAT_TARGET, LON_TARGET)
        st.download_button(
            label="🛸 Télécharger le fichier .KML pour le Drone",
            data=kml_data,
            file_name="mission_drone_tr4.kml",
            mime="application/vnd.google-earth.kml+xml",
            use_container_width=True
        )