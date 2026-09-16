import json
import os
import random
import time

def generate_pipeline_data():
    print("🚀 Running AgriSeq Edge AI Full Data Generator Pipeline...")

    # 1. Alerte Satellite (JSON)
    sat_data = {
        "parcel_id": "BAN_08 (Gharb)",
        "latitude": 34.3122,
        "longitude": -6.3548,
        "ndvi_mean": 0.32,
        "ndvi_baseline": 0.60,
        "impacted_area_m2": 250,
        "status": "ANOMALY_DETECTED",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("satellite_alert.json", "w") as f:
        json.dump(sat_data, f, indent=4)
    print("  [✓] satellite_alert.json generated.")

    # 2. Génome de référence NCBI TR4 fictif (FASTA)
    ncbi_seq = "ATGACGACGTACGTACGTACGTAAACCGGTTTTAAGGCCTTAAGGCCTTTGAAATTTGGGCCC" * 50
    with open("Fusarium_tr4_ncbi.fasta", "w") as f:
        f.write(">NCBI_AY220188.1 Fusarium oxysporum f. sp. cubense TR4\n")
        f.write(ncbi_seq + "\n")
    print("  [✓] Fusarium_tr4_ncbi.fasta generated.")

    # 3. Jeu de reads FASTQ locaux
    with open("agri_phytopathogen_reads.fastq", "w") as f:
        bases = ["A", "C", "G", "T"]
        for i in range(1, 1001):
            if i % 2 == 0:
                # Séquence avec match TR4
                seq = "ATGACGACG" + "".join(random.choices(bases, k=91))
            else:
                # Séquence environnementale neutre
                seq = "".join(random.choices(bases, k=100))
            f.write(f"@read_{i}_minion_run\n")
            f.write(f"{seq}\n")
            f.write("+\n")
            f.write("~" * 100 + "\n")
    print("  [✓] agri_phytopathogen_reads.fastq generated (1000 reads demo).")

    # 4. Rapport de Diagnostic Biologique (JSON)
    diag_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "gps_location": {
            "latitude": 34.3122,
            "longitude": -6.3548
        },
        "total_reads_processed": 70215,
        "tr4_aligned_reads": 29016,
        "infection_rate_percent": 41.32,
        "ai_confidence_score": 97.3,
        "pathogen_confirmed": True,
        "target_genome": "Fusarium oxysporum TR4 (NCBI AY220188.1)",
        "status": "POSITIVE_CONFIRMED"
    }
    with open("rapport_diagnostic.json", "w") as f:
        json.dump(diag_data, f, indent=4)
    print("  [✓] rapport_diagnostic.json generated.")

    # 5. Mission Drone KML (Xml/KML)
    kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Mission Epandage Biocontrol - Parcelle BAN_08</name>
    <Placemark>
      <name>Foyer TR4 Validé ADN</name>
      <description>Diagnostic : Fusarium TR4 (41.32% d'infection). Epandage ciblé sur rayon 15m.</description>
      <Point>
        <coordinates>-6.3548,34.3122,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>"""
    with open("mission_drone.kml", "w") as f:
        f.write(kml_content)
    print("  [✓] mission_drone.kml generated.")

    print("\n✅ All project assets updated successfully!")

if __name__ == "__main__":
    generate_pipeline_data()