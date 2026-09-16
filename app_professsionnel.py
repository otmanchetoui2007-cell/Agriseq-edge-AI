import os
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Configuration de la page
st.set_page_config(
    page_title="AgriSeq Edge — Control Center",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric {
        background-color: #1e222b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .status-card {
        background-color: #1e222b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2ecc71;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Chargement des données du pipeline
@st.cache_data
def load_data():
    json_path = "rapport_diagnostic.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"total_reads": 70215, "aligned_reads": 7797, "infection_rate": 11.10}

data = load_data()

# 3. Barre latérale (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/dna.png", width=64)
    st.title("AgriSeq Edge")
    st.caption("Système Nomade de Diagnostic Edge AI")
    st.divider()
    
    st.subheader("⚙️ État du Système")
    st.success("Dispositif : Orin Nano (Online)")
    st.info("Séquenceur : MinION Active")
    st.warning("Batterie : 84% (Autonomie ~6.5h)")
    
    st.divider()
    parcelle_selected = st.selectbox("Sélection de la Parcelle", ["BAN_07 (Souss-Massa)", "BAN_08 (Gharb)", "BAN_12 (Larrache)"])
    st.date_input("Date d'analyse", pd.to_datetime("today"))

# 4. En-tête principal
st.title("🛡️ Tableau de Bord — Surveillance & Diagnostic")
st.markdown(f"**Zone analysée :** `{parcelle_selected}` | **Statut d'exécution :** `Terminé (100%)`")

st.divider()

# 5. Métriques Clés (KPIs)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Reads Séquencés",
        value=f"{data.get('total_reads', 0):,}",
        delta="70.2k / 2h"
    )

with col2:
    st.metric(
        label="Reads Alignés (Cible)",
        value=f"{data.get('aligned_reads', 0):,}",
        delta="Couverture ITS"
    )

with col3:
    rate = data.get('infection_rate', 0)
    st.metric(
        label="Taux d'Infection Global",
        value=f"{rate:.2f} %",
        delta="Seuil critique > 5%",
        delta_color="inverse" if rate > 5 else "normal"
    )

with col4:
    st.metric(
        label="Indice de Confiance IA",
        value="96.4 %",
        delta="TorchScript Model"
    )

st.divider()

# 6. Visualisations Principales
tab1, tab2, tab3, tab4 = st.tabs(["⚡ Temps Réel (Live)", "🗺️ Cartographie", "📊 Analyses Génomiques", "🌡️ Capteurs IoT"])
with tab1:
    col_map, col_info = st.columns([2, 1])
    
    # Données géographiques fictives
    map_df = pd.DataFrame({
        'lat': [30.420, 30.422, 30.425, 30.421, 30.424],
        'lon': [-9.598, -9.595, -9.592, -9.590, -9.596],
        'Infection': [2.1, 11.1, 4.5, 1.2, 12.8],
        'Statut': ['Faible', 'Élevé', 'Moyen', 'Faible', 'Élevé']
    })
    
    with col_map:
        fig_map = px.scatter_mapbox(
            map_df,
            lat="lat",
            lon="lon",
            color="Statut",
            size="Infection",
            color_discrete_map={"Élevé": "#e74c3c", "Moyen": "#f1c40f", "Faible": "#2ecc71"},
            zoom=13,
            mapbox_style="carto-darkmatter",
            title="Carte de Pression Pathogène (Heatmap Spatiale)"
        )
        fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template="plotly_dark")
        st.plotly_chart(fig_map, use_container_width=True)
        
    with col_info:
        st.subheader("🎯 Recommandation Agronomique")
        st.markdown("""
        <div class="status-card">
            <h4>Action Immédiate Requise</h4>
            <p>Détection confirmée sur les points de prélèvement <b>BAN_07_B</b> et <b>BAN_07_E</b>.</p>
            <ul>
                <li><b>Traitement :</b> Pulvérisation ciblée de biocontrôle.</li>
                <li><b>Périmètre :</b> Rayon de 15 mètres autour du foyer.</li>
                <li><b>Économie d'intrants :</b> -85% par rapport à un traitement global.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    c1, c2 = st.columns(2)
    
    with c1:
        # Pie Chart d'alignement
        aligned = data.get('aligned_reads', 0)
        unaligned = data.get('total_reads', 1) - aligned
        
        fig_pie = px.pie(
            names=['Séquences Alignées', 'Autres / Hôte'],
            values=[aligned, unaligned],
            color_discrete_sequence=['#e74c3c', '#2ecc71'],
            title="Distribution du Séquençage",
            hole=0.4
        )
        fig_pie.update_layout(template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        # Couverture de la référence
        x_ref = np.linspace(0, 1678, 100)
        y_cov = np.sin(x_ref / 100) * 50 + 100 + np.random.normal(0, 10, 100)
        
        fig_cov = px.area(
            x=x_ref, y=y_cov,
            labels={'x': 'Position sur le gène cible (pb)', 'y': 'Profondeur de lecture (X)'},
            title="Profondeur de Couverture de la Référence (1678 bp)"
        )
        fig_cov.update_traces(line_color="#3498db")
        fig_cov.update_layout(template="plotly_dark")
        st.plotly_chart(fig_cov, use_container_width=True)

with tab3:
    # Graphique temporel des conditions micro-climatiques
    dates = pd.date_range(end=pd.Timestamp.now(), periods=24, freq='H')
    iot_df = pd.DataFrame({
        'Heure': dates,
        'Température (°C)': np.random.normal(28, 2, 24),
        'Humidité Sol (%)': np.random.normal(72, 3, 24),
        'Humidité Air (%)': np.random.normal(85, 4, 24)
    })
    
    fig_iot = px.line(
        iot_df, x='Heure', y=['Température (°C)', 'Humidité Sol (%)', 'Humidité Air (%)'],
        title="Télémétrie des Capteurs IoT (Dernières 24 Heures)"
    )
    fig_iot.update_layout(template="plotly_dark")
    st.plotly_chart(fig_iot, use_container_width=True)
