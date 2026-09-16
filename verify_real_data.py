import os
import pod5

def parse_fastq(fastq_path):
    reads = {}
    if not os.path.exists(fastq_path):
        return reads
        
    with open(fastq_path, 'r', encoding='utf-8', errors='ignore') as f:
        while True:
            header = f.readline()
            if not header:
                break
            seq = f.readline().strip()
            f.readline() # Ligne '+'
            f.readline() # Ligne Qualité
            
            read_id = header.split()[0][1:]
            reads[read_id] = seq
    return reads

def check_dataset():
    pod5_dir = "data_agri/raw"
    fastq_dir = "data_agri/basecalls"
    
    fastq_files = [os.path.join(fastq_dir, f) for f in os.listdir(fastq_dir) if f.endswith('.fastq')]
    ground_truth = {}
    for fq in fastq_files:
        ground_truth.update(parse_fastq(fq))
        
    print("=== Vérification du Dataset Fongique Réel ===")
    print(f"Séquences de référence FASTQ chargées : {len(ground_truth)}")
    
    pod5_files = [os.path.join(pod5_dir, f) for f in os.listdir(pod5_dir) if f.endswith('.pod5')]
    total_signals = 0
    matched_signals = 0
    corrupted_files = 0
    
    for p5 in pod5_files:
        try:
            with pod5.Reader(p5) as reader:
                for record in reader.reads():
                    total_signals += 1
                    read_id = str(record.read_id)
                    if read_id in ground_truth:
                        matched_signals += 1
                        if matched_signals == 1:
                            signal_len = len(record.signal)
                            target_seq = ground_truth[read_id]
                            print(f"\n[Exemple de Read Validé]")
                            print(f"Read ID          : {read_id}")
                            print(f"Longueur Signal  : {signal_len} points")
                            print(f"Séquence Vraie   : {target_seq[:50]}... (Longueur: {len(target_seq)} bases)")
        except Exception:
            corrupted_files += 1
            print(f"[Avertissement] Fichier incomplet ignoré : {os.path.basename(p5)}")

    print("\n=== Bilan du Dataset ===")
    print(f"Signaux bruts POD5 valides : {total_signals}")
    print(f"Signaux appariés (POD5 <-> FASTQ) : {matched_signals}")
    print(f"Fichiers corrompus/ignorés : {corrupted_files}")

if __name__ == "__main__":
    check_dataset()
