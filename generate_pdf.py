import json
import os
import datetime

def generate_audit_report():
    # 1. Vérification de la présence des fichiers du pipeline
    if not (os.path.exists("satellite_alert.json") and os.path.exists("rapport_diagnostic.json")):
        print("⚠️ Données incomplètes pour générer le rapport d'audit.")
        return

    with open("satellite_alert.json", "r") as f:
        sat_data = json.load(f)
    with open("rapport_diagnostic.json", "r") as f:
        dna_data = json.load(f)

    # 2. Structure du registre de biosécurité
    audit_log = {
        "report_id": f"REP-TR4-{datetime.datetime.now().strftime('%Y%m%d-%H%M')}",
        "execution_date": datetime.datetime.now().isoformat(),
        "parcel": sat_data["parcel_id"],
        "gps_target": [sat_data["latitude"], sat_data["longitude"]],
        "initial_ndvi_stress": sat_data["ndvi_mean"],
        "dna_confirmation": {
            "pathogen": dna_data["target_genome"],
            "infection_rate": f"{dna_data['infection_rate_percent']}%",
            "confidence": f"{dna_data['ai_confidence_score']}%"
        },
        "drone_intervention": {
            "status": "EXECUTED",
            "treatment_radius_m": 15,
            "product_applied": "Pseudomonas protegens (Biocontrôle)",
            "volume_saved_percent": 92.0
        },
        "post_monitoring_scheduled": (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    }

    # 3. Sauvegarde de l'audit au format JSON (consommable par export_cdcf_pdf.py)
    with open("audit_biosecurite_final.json", "w", encoding="utf-8") as f:
        json.dump(audit_log, f, indent=4)

    print(f"✅ Audit de Biosécurité généré : 'audit_biosecurite_final.json'")
    print(f"📅 Prochain contrôle satellite programmé pour le : {audit_log['post_monitoring_scheduled']}")

if __name__ == "__main__":
    generate_audit_report()