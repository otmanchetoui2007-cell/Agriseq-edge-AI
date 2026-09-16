# export_cdcf_pdf.py
import os
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
except ImportError:
    os.system("pip install reportlab")
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors

def generate_pdf():
    pdf_filename = "Cahier_des_Charges_AgriSeq_Edge.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = []

    # Styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#1e293b'))
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.HexColor('#0284c7'), spaceBefore=10, spaceAfter=4)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=colors.HexColor('#334155'))

    # Title Header
    story.append(Paragraph("<b>CAHIER DES CHARGES — AGRISEQ EDGE</b>", title_style))
    story.append(Paragraph("Plateforme de Recherche en Agriculture de Précision & Deep Learning Nomade", h2_style))
    story.append(Spacer(1, 8))

    # Section 1
    story.append(Paragraph("<b>1. CONTEXTE ET OBJECTIFS DE RECHERCHE</b>", h2_style))
    story.append(Paragraph("• <b>Problématique :</b> Réduction du temps de diagnostic de <i>Fusarium oxysporum TR4</i> de 3 semaines à moins de 5 minutes via Edge AI.<br/>• <b>Périmètre Géo :</b> Zones agricoles au Maroc (Gharb, Larache, Souss-Massa).", body_style))
    story.append(Spacer(1, 6))

    # Section 2
    story.append(Paragraph("<b>2. SPÉCIFICATIONS FONCTIONNELLES</b>", h2_style))
    table_data = [
        ["Pilier", "Composant", "Données Entrée", "Données Sortie"],
        ["1. Télédétection", "fetch_satellite.py", "API Sentinel-2 / BBox", "satellite_alert.json"],
        ["2. Basecalling IA", "infer.py / model.pt", "Signal brut (.pod5)", "Séquences (.fastq)"],
        ["3. Alignement ADN", "run_align_pure.py", ".fastq + reference.fasta", "rapport_diagnostic.json"],
        ["4. Drone", "generate_kml.py", "GPS Foyer Anomalie", "mission_drone.kml"],
        ["5. Interface", "app_main.py", "JSON / FASTQ", "Dashboard Streamlit"]
    ]
    t = Table(table_data, colWidths=[70, 100, 120, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

    # Section 3
    story.append(Paragraph("<b>3. SPÉCIFICATIONS TECHNIQUES</b>", h2_style))
    story.append(Paragraph("• <b>Matériel Cible :</b> Edge AI (NVIDIA Jetson Orin Nano / PC Portable Nomade).<br/>• <b>Deep Learning :</b> Framework PyTorch (Modèle hybride CRNN/CNN-LSTM).<br/>• <b>Bio-informatique :</b> Alignement k-mers (k=9) en Python pur contre la référence NCBI AY520188.1.", body_style))
    story.append(Spacer(1, 6))

    # Section 4
    story.append(Paragraph("<b>4. CRITÈRES DE VALIDATION SCIENTIFIQUE</b>", h2_style))
    story.append(Paragraph("• Temps total d'exécution du pipeline master < 5 minutes en local.<br/>• Sensibilité de détection génétique > 95% sur les séquences d'infection TR4.<br/>• Économie de phytosanitaires > 80% via l'épandage ciblé par fichier .KML.", body_style))

    doc.build(story)
    print(f"✅ Fichier PDF généré avec succès : {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()