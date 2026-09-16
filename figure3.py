import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Génération de la Figure avec emplacement pour Photos Réelles
def create_figure_with_photos():
    fig, ax = plt.subplots(figsize=(9, 3.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)

    # Fonction pour dessiner les blocs matériels
    def draw_hardware_card(x, y, w, h, title, subtitle, border_color):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", 
                                      linewidth=1.5, edgecolor=border_color, facecolor="#ffffff")
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.25, title, fontsize=8, fontweight='bold', ha='center', color=border_color)
        ax.text(x + w/2, y + 0.25, subtitle, fontsize=6.5, ha='center', color="#555555")

    # Emplacements Matériels (Cartes)
    draw_hardware_card(0.3, 0.8, 2.5, 3.4, "1. Sequenceur MinION", "Oxford Nanopore (USB-C)", "#1f77b4")
    draw_hardware_card(3.75, 0.8, 2.5, 3.4, "2. Unite Edge", "NVIDIA Jetson / PC Terrain", "#004529")
    draw_hardware_card(7.2, 0.8, 2.5, 3.4, "3. Drone Agricole", "Station Sol / Trajectoire", "#d62728")

    # Simulation / Chargement des visuels matériels (Cadres photo)
    for cx, col in zip([1.55, 5.0, 8.45], ["#e0f2fe", "#dcce20", "#fee2e2"]):
        photo_box = patches.FancyBboxPatch((cx-0.9, 1.3), 1.8, 1.8, boxstyle="square,pad=0", 
                                           facecolor=col, edgecolor="none", alpha=0.5)
        ax.add_patch(photo_box)

    # Annotations sur les zones photo
    ax.text(1.55, 2.2, "[ Photo MinION ]", fontsize=7, ha='center', color="#0369a1", fontweight='bold')
    ax.text(5.0, 2.2, "[ Photo Jetson / PC ]", fontsize=7, ha='center', color="#15803d", fontweight='bold')
    ax.text(8.45, 2.2, "[ Photo Drone ]", fontsize=7, ha='center', color="#b91c1c", fontweight='bold')

    # Flèches de connexion corrigées (sans chevauchement)
    # Arrow 1: MinION -> Edge
    ax.annotate("", xy=(3.65, 2.5), xytext=(2.9, 2.5),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.5", lw=2, color="#1f77b4"))
    ax.text(3.27, 2.8, "USB-C 3.0\n(.pod5 / pA)", fontsize=6.5, fontweight='bold', ha='center', color="#1f77b4")

    # Arrow 2: Edge -> Drone
    ax.annotate("", xy=(7.1, 2.5), xytext=(6.35, 2.5),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.5", lw=2, color="#d62728"))
    ax.text(6.72, 2.8, "MAVLink / Radio\n(.KML)", fontsize=6.5, fontweight='bold', ha='center', color="#d62728")

    plt.title("Figure 3 — Chaine Materielle Embarquee de Terrain (Hardware Setup)", fontsize=9.5, fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig("fig3_photos_temp.png", dpi=300, bbox_inches='tight')
    plt.close()

# 2. Construction du PDF
def generate_pdf():
    create_figure_with_photos()
    pdf_filename = "Figure3_Hardware_Setup_Photos.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=15, textColor=colors.HexColor("#004529"), spaceAfter=10)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=8.5, leading=11, spaceAfter=8)

    elements = []
    elements.append(Paragraph("AgriSeq Edge - Configuration Matérielle Réelle", title_style))
    elements.append(RLImage("fig3_photos_temp.png", width=500, height=194))
    elements.append(Spacer(1, 10))

    legend = "<b>Figure 3 — Configuration matérielle et flux d'acquisition sur le terrain :</b> (1) Séquenceur Oxford Nanopore MinION connecté en USB-C 3.0 à (2) l'unité de calcul embarquée NVIDIA Jetson / PC de terrain exécutant l'inférence PyTorch. (3) Transmission sans fil du fichier de mission .KML au drone agricole pour traitement localisé."
    elements.append(Paragraph(legend, body_style))

    doc.build(elements)
    if os.path.exists("fig3_photos_temp.png"):
        os.remove("fig3_photos_temp.png")
    print("PDF généré avec succès !")

if __name__ == "__main__":
    generate_pdf()