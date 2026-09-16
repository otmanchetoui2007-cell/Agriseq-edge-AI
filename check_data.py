import pod5, numpy as np, glob, os

# Recherche dans le dossier local ET le dossier parent
pod5_files = glob.glob(os.path.join("real_pod5", "**", "*.pod5"), recursive=True) + glob.glob(os.path.join("..", "real_pod5", "**", "*.pod5"), recursive=True)

if not pod5_files:
    print(" [ATTENTION] Aucun fichier .pod5 valide trouve. Le telechargement S3 est probablement encore en cours.")
else:
    target_file = pod5_files[0]
    print(f"Fichier detecte : {target_file}\n")
    with pod5.Reader(target_file) as reader:
        for read_record in reader.reads():
            raw_signal = read_record.signal
            print("=== Validation Ingestion Signal POD5 ===")
            print(f"ID du brin d'ADN    : {read_record.read_id}")
            print(f"Nombre de mesures   : {len(raw_signal)}")
            print(f"Plage d'intensite   : Min = {np.min(raw_signal):.2f} pA | Max = {np.max(raw_signal):.2f} pA")
            print(f"5 premiers points   : {raw_signal[:5]}")
            break
