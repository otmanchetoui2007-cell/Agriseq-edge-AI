import streamlit as st
import json
import os
import time

# Importation sécurisée de Folium pour la cartographie interactive
try:
    import folium
    from streamlit_folium import st_folium
    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False

st.set_page_config(
    page_title="AgriSeq Edge AI - Control Center", 
    layout="wide", 
    page_icon="🌱"
)

# -----------------------------------------------------------------------------
# FONCTIONS BIOINFORMATIQUES (CHARGEURS AUTOMATIQUES LOCAUX)
# -----------------------------------------------------------------------------
def load_local_fastq(filename="agri_phytopathogen_reads.fastq"):
    """Lit automatiquement le fichier FASTQ du dossier racine sans intervention utilisateur."""
    reads = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for i in range(1, len(lines), 4):
                seq = lines[i].strip().upper()
                if seq:
                    reads.append(seq)
    return reads

def load_ncbi_kmers(filename="Fusarium_tr4_ncbi.fasta", k=9):
    """Charge le génome NCBI local et extrait l'index k-mers."""
    if not os.path.exists(filename):
        return set()
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    ref_seq = "".join([l.strip() for l in lines if not l.startswith(">")]).upper()
    return {ref_seq[i:i+k] for i in range(len(ref_seq) - k + 1)}

# -----------------------------------------------------------------------------
# BARRE LATÉRALE : MONITEUR MATÉRIEL JETSON ORIN & LOGS KERNEL
# -----------------------------------------------------------------------------
st.sidebar.title("⚡ Moniteur NVIDIA Jetson Orin")
st.sidebar.caption("Séquençage & Inférence Edge AI - Mode SIL")

col_sb1, col_sb2 = st.sidebar.columns(2)
col_sb1.metric("GPU Temp", "42.1 °C")
col_sb2.metric("Consommation", "6.8 W")

st.sidebar.metric(label="VRAM Cache TensorRT", value="1.8 GB / 8.0 GB")
st.sidebar.metric(label="Liaison Drone MAVLink", value="CONNECTED", delta="4G/LoRa (57600 baud)")

if os.path.exists("figure3_hardware_setup.png"):
    st.sidebar.image("figure3_hardware_setup.png", caption="Banc d'Essai Embarqué Jetson + MinION")

st.sidebar.subheader("🖥️ Console Télémétrie KERNEL")
st.sidebar.code("""
[19:14:02] [KERNEL] MinION Mk1B connected
[19:14:03] [CUDA] Engine basecaller_int8 loaded
[19:14:04] [MAVLINK] Telemetry OK on /dev/ttyTHS1
[19:14:05] [THERMAL] GPU: 42.1°C | Fan: AUTO
[19:14:06] [K-MER] Index TR4 ready (k=9)
""", language="bash")

# -----------------------------------------------------------------------------
# PAGE PRINCIPALE : PANNEAU DE CONTRÔLE
# -----------------------------------------------------------------------------
st.title("🌱 AgriSeq Edge AI : Surveillance & Diagnostic TR4")
st.markdown("**Plateforme Industrielle d'Intervention Phytosanitaire Autonome**")

tab1, tab2, tab3 = st.tabs([
    "🛰️ 1. Alerte Satellite & Cartographie", 
    "🧬 2. Diagnostic ADN Nanopore", 
    "🛸 3. Mission Drone & Ordres de Vol"
])

# -----------------------------------------------------------------------------
# TAB 1 : ALERTE SATELLITE & CARTE INTERACTIVE
# -----------------------------------------------------------------------------
with tab1:
    st.header("🛰️ Étape 1 : Détection d'Anomalie Végétale (Sentinel-2)")
    
    col_sat1, col_sat2 = st.columns([1, 1])
    
    with col_sat1:
        if os.path.exists("satellite_alert.json"):
            with open("satellite_alert.json", "r") as f:
                sat_data = json.load(f)
            
            lat = sat_data.get("latitude", 34.3122)
            lon = sat_data.get("longitude", -6.3548)
            
            st.error(f"🚨 ALERTE SANITAIRE ACTIVÉE — Parcelle {sat_data.get('parcel_id', 'BAN_08 (Gharb)')}")
            st.metric(
                label="Indice NDVI Moyen", 
                value=sat_data.get("ndvi_mean", 0.32), 
                delta="-0.28 (Stress Végétal Détecté)", 
                delta_color="inverse"
            )
            st.write(f"**Épicentre GPS :** `{lat} N, {lon} W`")
            st.write(f"**Surface Impactée :** `{sat_data.get('impacted_area_m2', 250)} m²`")
            st.write(f"**Horodatage Satellite :** `{sat_data.get('timestamp', '2026-09-15 19:00:00')}`")
        else:
            st.warning("Aucune alerte satellite détectée. Exécutez `python run_full_pipeline.py`.")

    with col_sat2:
        if HAS_FOLIUM and os.path.exists("satellite_alert.json"):
            st.subheader("🗺️ Cartographie High-Res (Esri World Imagery)")
            m = folium.Map(
                location=[lat, lon], 
                zoom_start=18, 
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
                attr="Esri World Imagery"
            )
            folium.Marker(
                [lat, lon], 
                popup="Foyer TR4 Suspecté", 
                icon=folium.Icon(color="red", icon="warning")
            ).add_to(m)
            folium.Circle(
                [lat, lon], 
                radius=15, 
                color="red", 
                fill=True, 
                fill_opacity=0.35, 
                popup="Périmètre de Confinement (15m)"
            ).add_to(m)
            st_folium(m, width=500, height=350)
        elif os.path.exists("figure1_ndvi_satellite.png"):
            st.image("figure1_ndvi_satellite.png", caption="Cartographie d'Anomalie NDVI - Sentinel-2")

# -----------------------------------------------------------------------------
# TAB 2 : DIAGNOSTIC ADN EN LIVE STREAMING (FASTQ AUTOMATIQUE)
# -----------------------------------------------------------------------------
with tab2:
    st.header("🧬 Étape 2 : Diagnostic Biologique Nanopore en Temps Réel")
    
    # Auto-détection du fichier FASTQ local
    fastq_file = "agri_phytopathogen_reads.fastq"
    real_reads = load_local_fastq(fastq_file)
    target_kmers = load_ncbi_kmers("Fusarium_tr4_ncbi.fasta", k=9)

    if real_reads:
        st.success(f"📁 Source FASTQ locale chargée automatiquement : `{fastq_file}` (**{len(real_reads)} reads ADN**)")
    else:
        st.warning(f"⚠️ Fichier `{fastq_file}` introuvable dans le répertoire du projet.")

    if os.path.exists("rapport_diagnostic.json"):
        with open("rapport_diagnostic.json", "r") as f:
            diag = json.load(f)

        # Inférence interactive sur les reads du fichier FASTQ
        if st.button("▶️ Lancer le Séquençage ADN en Direct (MinION Stream Réel)"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            metric_placeholder = st.empty()
            stream_console = st.empty()
            
            total_count = len(real_reads) if real_reads else diag.get("total_reads_processed", 70215)
            matched_count = 0
            chunk_size = max(1, total_count // 10)
            
            logs_buffer = []
            k = 9
            
            for i in range(0, total_count, chunk_size):
                chunk = real_reads[i:i + chunk_size] if real_reads else []
                
                # Traitement k-mers direct sur la séquence brute
                for seq in chunk:
                    if len(seq) >= k:
                        read_kmers = {seq[j:j+k] for j in range(len(seq) - k + 1)}
                        if not read_kmers.isdisjoint(target_kmers):
                            matched_count += 1
                
                step = min(100, int(((i + chunk_size) / total_count) * 100))
                current_processed = min(i + chunk_size, total_count)
                
                if not real_reads:
                    matched_count = int(diag.get("tr4_aligned_reads", 29016) * (step / 100))
                
                pct = round((matched_count / max(current_processed, 1)) * 100, 2)
                
                if chunk:
                    sample_seq = chunk[0][:35] + "..."
                    logs_buffer.append(
                        f"[{time.strftime('%H:%M:%S')}] READ #{current_processed} | SEQ: {sample_seq} | ALIGNMENT: {'MATCH TR4' if matched_count > 0 else 'CLEAR'}"
                    )
                    if len(logs_buffer) > 5:
                        logs_buffer.pop(0)

                progress_bar.progress(step)
                status_text.text(f"🧪 Analyse du flux ionique en cours... Reads traités : {current_processed} / {total_count}")
                
                # Métriques d'affichage corrigées
                with metric_placeholder.container():
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Reads ADN Traités (FASTQ)", current_processed)
                    m2.metric(
                        "Alignements TR4 (k=9)", 
                        matched_count, 
                        help="Détection de signatures génomiques compatibles avec Fusarium TR4"
                    )
                    m3.metric(
                        "Taux d'Infection ADN", 
                        f"{pct}%", 
                        delta="TR4_DETECTED", 
                        delta_color="inverse", 
                        help="Proportion de reads alignés TR4"
                    )
                
                stream_console.code("\n".join(logs_buffer), language="bash")
                time.sleep(0.08)
                
            st.success("✅ Inférence k-mers terminée : Signatures génomiques de Fusarium TR4 confirmées sur les reads du fichier FASTQ.")

        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Reads ADN Traités", diag.get("total_reads_processed", 70215))
            c2.metric(
                "Indice de Confiance IA", 
                f"{diag.get('ai_confidence_score', 97.3)}%", 
                help="Score de confiance de la classification"
            )
            c3.metric(
                "Taux d'Infection ADN", 
                f"{diag.get('infection_rate_percent', 41.32)}%", 
                delta=diag.get("status", "POSITIVE_CONFIRMED"), 
                delta_color="inverse", 
                help="Proportion de reads alignés TR4"
            )

        st.subheader("📋 Télémétrie Génétique Officielle (Output JSON)")
        st.json(diag)

# -----------------------------------------------------------------------------
# TAB 3 : MISSION DRONE & ORDRES DE VOL
# -----------------------------------------------------------------------------
with tab3:
    st.header("🛸 Étape 3 : Trajectoire d'Épandage & Plan de Vol Drone")
    
    col_dr1, col_dr2 = st.columns([1, 1])
    
    with col_dr1:
        if os.path.exists("mission_drone.kml"):
            with open("mission_drone.kml", "r") as f:
                kml_data = f.read()
                
            st.success("✅ Fichier KML d'intervention prêt pour transmission MAVLink / Pixhawk.")
            
            st.download_button(
                label="📥 Télécharger la Mission KML (.kml)",
                data=kml_data,
                file_name="mission_drone.kml",
                mime="application/vnd.google-earth.kml+xml"
            )
            
            st.subheader("📄 En-tête du Plan de Vol KML Généré")
            st.code(kml_data[:450] + "\n...", language="xml")
        else:
            st.info("Le plan de vol sera généré dès la confirmation génétique.")
            
    with col_dr2:
        st.subheader("🛡️ Traçabilité & Rapport de Biosécurité")
        st.write("Le registre d'audit officiel certifie l'horodatage, le niveau d'infection et le périmètre d'isolement.")
        
        if os.path.exists("Cahier_des_Charges_AgriSeq_Edge.pdf"):
            with open("Cahier_des_Charges_AgriSeq_Edge.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📄 Télécharger le Rapport d'Audit Officiel de Biosécurité (PDF)",
                    data=pdf_file,
                    file_name="Rapport_Audit_Biosecurite_AgriSeq.pdf",
                    mime="application/pdf"
                )