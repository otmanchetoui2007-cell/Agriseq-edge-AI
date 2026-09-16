import json
import time
import random

def emulate_nanopore_signal():
    """Simule la sortie brute du séquenceur MinION en mémoire."""
    print("🔌 [EMULATEUR] MinION connecté sur USB-C (Émulation)")
    print("🧪 [EMULATEUR] Traitement du flux ionique pA en cours...")
    time.sleep(1)
    
    # Génération d'un read synthétique avec présence du pathogène TR4
    return {
        "read_id": f"read_{random.randint(1000, 9999)}",
        "raw_signal_length": 1024,
        "simulated_sequence": "AACGCACACTCACACTCACACTCACACTCACACACGAATTATACCACACACAGATTTATATCG",
        "mean_qscore": 17.5
    }

def emulate_drone_telemetry(lat, lon):
    """Simule la télémétrie MAVLink du drone en stationnaire."""
    print(f"🛸 [EMULATEUR] Liaison radio Drone 4G/MAVLink établie à [{lat}, {lon}]")
    return {
        "battery_percent": 98,
        "gps_fix": 3,
        "target_coordinates": [lat, lon],
        "status": "ARMED_AND_READY"
    }

if __name__ == "__main__":
    print("=== DEMARRAGE DE L'EMULATEUR MATERIEL SIL ===")
    read_data = emulate_nanopore_signal()
    drone_data = emulate_drone_telemetry(34.3122, -6.3548)
    
    with open("hardware_status.json", "w") as f:
        json.dump({"nanopore": read_data, "drone": drone_data}, f, indent=4)
        
    print("✅ Signaux matériels simulés avec succès dans 'hardware_status.json'")