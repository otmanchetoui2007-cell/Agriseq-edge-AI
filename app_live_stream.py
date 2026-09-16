import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# 1. Style CSS ciblé (Thème sombre Cyber/Edge AI)
st.markdown("""
    <style>
    .live-card {
        background-color: #11151c;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .seq-box {
        background-color: #0d1117;
        font-family: 'Courier New', monospace;
        padding: 12px;
        border-radius: 6px;
        border: 1px solid #30363d;
        line-height: 1.6;
        word-break: break-all;
    }
    .base-m { color: #2ecc71; font-weight: bold; } /* Match */
    .base-s { color: #e67e22; font-weight: bold; } /* Substitution */
    .base-i { color: #3498db; font-weight: bold; } /* Insertion */
    .base-d { color: #f1c40f; font-weight: bold; } /* Déletion */
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 4px 0;
        border-bottom: 1px solid #21262d;
        font-size: 0.9em;
    }
    </style>
""", unsafe_allow_html=True)

# 2. En-tête Live
col_title, col_status = st.columns([3, 1])
with col_title:
    st.subheader("⚡ DASHBOARD TEMPS RÉEL")
with col_status:
    st.markdown("🟢 **EN COURS** &nbsp;&nbsp; `00:12:45`", unsafe_allow_html=True)

# --- RANGÉE 1 : SIGNAL BRUT & SÉQUENCE EN DIRECT ---
col_sig, col_seq = st.columns(2)

with col_sig:
    st.markdown('<div class="live-card"><b>📉 Signal Brut en Temps Réel (pA)</b>', unsafe_allow_html=True)
    
    # Simulation du signal d'intensité pA (Nanopore Pod5)
    t = np.linspace(0, 30, 300)
    signal_pa = 40 * np.sin(t) + np.random.normal(0, 25, 300)
    
    fig_sig = go.Figure()
    fig_sig.add_trace(go.Scatter(x=t, y=signal_pa, mode='lines', line=dict(color='#3498db', width=1)))
    fig_sig.update_layout(
        height=180, margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Temps (s)", showgrid=True, gridcolor="#21262d"),
        yaxis=dict(title="pA", range=[-120, 120], showgrid=True, gridcolor="#21262d"),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#8b949e")
    )
    st.plotly_chart(fig_sig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_seq:
    st.markdown('<div class="live-card"><b>🧬 Séquence Décodée (Live)</b>', unsafe_allow_html=True)
    st.caption("Confiance moyenne: **92.7%**")
    
    seq_html = """
    <div class="seq-box">
        <span class="base-m">ACGTACGATTCGGTACGTAGCTAGCTAGCT</span><br>
        <span class="base-m">TAGCTAGGCTAACGTTAGCTAGCTAGCTAG</span><br>
        <span class="base-m">GCTAGCTAGCTAGCTAGCTAGCTAGCTAGC</span><br>
        <span class="base-s">TAGCTAG</span><span class="base-m">CTAGCTAGCTAGCTAGCTA</span><br>
        <span style="color:#8b949e">...</span>
    </div>
    """
    st.markdown(seq_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- RANGÉE 2 : VARIANTS & PERFORMANCE MATÉRIELLE ---
col_var, col_perf = st.columns(2)

with col_var:
    st.markdown('<div class="live-card"><b>🔍 Détection de Variants (Temps Réel)</b>', unsafe_allow_html=True)
    st.markdown('<span class="base-m">■ Match</span> &nbsp; <span class="base-s">■ Substitution</span> &nbsp; <span class="base-i">■ Insertion</span> &nbsp; <span class="base-d">■ Délétion</span>', unsafe_allow_html=True)
    
    ref_txt = "Référence : ACGTACGATTCGGTACGTAGCTAGCTAGCT"
    obs_txt = "Échantillons: ACGTACGATTTGGTACGTAGTTAGCTAGCT"
    
    st.markdown(f'<div class="seq-box" style="font-size:0.85em;">{ref_txt}<br>{obs_txt}</div>', unsafe_allow_html=True)
    
    v1, v2, v3 = st.columns(3)
    v1.metric("Substitution", "1", delta_color="off")
    v2.metric("Insertion", "1", delta_color="off")
    v3.metric("Délétion", "1", delta_color="off")
    st.markdown('</div>', unsafe_allow_html=True)

with col_perf:
    st.markdown('<div class="live-card"><b>🖥️ Qualité & Performance (Orin Nano)</b>', unsafe_allow_html=True)
    
    metrics = [
        ("Q-score moyen", "15.6"),
        ("Bases appelées", "112,540"),
        ("Vitesse", "85.4 bases/s"),
        ("Latence (ms)", "12.4"),
        ("CPU Usage", "28%"),
        ("RAM Usage", "1.8 / 8 GB"),
        ("GPU Usage (Orin)", "35%"),
        ("Température", "48 °C")
    ]
    
    for label, val in metrics:
        st.markdown(f'<div class="metric-row"><span>{label}</span><b>{val}</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- RANGÉE 3 : GESTION & VÉRIFICATION DES MODIFICATIONS ---
col_edit, col_val = st.columns(2)

with col_edit:
    st.markdown('<div class="live-card"><b>🛠️ Gestion de Modification</b>', unsafe_allow_html=True)
    st.text_input("Cible sélectionnée", "... A C G A T T G G T A A C G ...", disabled=True)
    st.text_input("Modification souhaitée", "... A C G A T C G G T A A C G ...")
    
    c_t, c_m = st.columns(2)
    with c_t:
        st.selectbox("Type", ["Substitution (T → C)", "Insertion", "Délétion"])
    with c_m:
        st.selectbox("Méthode", ["Base Editing (BE4max)", "Prime Editing", "CRISPR-Cas9"])
        
    st.button("EXÉCUTER MODIFICATION", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

with col_val:
    st.markdown('<div class="live-card"><b>✅ Vérification Après Modification</b>', unsafe_allow_html=True)
    
    # Donut Chart de statut
    fig_gauge = go.Figure(go.Pie(
        values=[76, 24],
        hole=0.75,
        marker_colors=['#2ecc71', '#21262d'],
        textinfo='none'
    ))
    fig_gauge.update_layout(
        height=120, margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text='76%', x=0.5, y=0.5, font_size=20, showarrow=False, font_color="#ffffff")]
    )
    
    col_g, col_txt = st.columns([1, 2])
    with col_g:
        st.plotly_chart(fig_gauge, use_container_width=True)
    with col_txt:
        st.markdown("<b>Statut :</b> <span style='color:#f1c40f'>En cours...</span>", unsafe_allow_html=True)
        st.markdown("<b>Résultat attendu :</b> T → C", unsafe_allow_html=True)
        st.markdown("<b>Résultat observé :</b> T → C ✓", unsafe_allow_html=True)
        st.markdown("<b>Confiance :</b> 97.3%", unsafe_allow_html=True)
        
    st.button("MODIFICATION VALIDÉE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)