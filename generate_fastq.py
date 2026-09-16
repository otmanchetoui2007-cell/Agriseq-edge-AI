import os
import pod5
import torch
import numpy as np
from train import ctc_decode

def export_to_fastq_v2(pod5_dir="data_agri/raw", output_fastq="agri_phytopathogen_reads.fastq"):
    if not os.path.exists("basecaller_model.pt"):
        print("Erreur : Fichier basecaller_model.pt introuvable.")
        return

    model = torch.jit.load("basecaller_model.pt")
    model.eval()
    
    pod5_files = [os.path.join(pod5_dir, f) for f in os.listdir(pod5_dir) if f.endswith('.pod5')]
    total_reads = 0
    offset = 1024
    window_size = 2048
    
    print(f"=== Génération Haute Précision du Fichier FASTQ ===")
    print(f"Dossier source : {pod5_dir}")
    
    with open(output_fastq, "w", encoding="utf-8") as fq_out:
        for p5 in pod5_files:
            try:
                with pod5.Reader(p5) as reader:
                    for record in reader.reads():
                        raw_signal = record.signal.astype(np.float32)
                        
                        if len(raw_signal) < (offset + window_size):
                            continue
                            
                        signal_chunk = raw_signal[offset : offset + window_size]
                        
                        mean, std = np.mean(signal_chunk), np.std(signal_chunk)
                        if std == 0: continue
                        norm_signal = (signal_chunk - mean) / std
                        
                        input_tensor = torch.tensor(norm_signal, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
                        
                        with torch.no_grad():
                            log_probs = model(input_tensor)
                        pred_seq = ctc_decode(log_probs)[0]
                        
                        if len(pred_seq) >= 15:
                            read_id = str(record.read_id)
                            # Assignation d'un score de qualité Q30/Q40 fictif ('I') pour compatibilité FASTQ
                            quality_scores = "I" * len(pred_seq)
                            
                            fq_out.write(f"@{read_id}\n")
                            fq_out.write(f"{pred_seq}\n")
                            fq_out.write("+\n")
                            fq_out.write(f"{quality_scores}\n")
                            
                            total_reads += 1
                            if total_reads % 1000 == 0:
                                print(f"-> {total_reads} reads convertis avec succès...")
            except Exception:
                continue

    print(f"\n Succès ! {total_reads} reads convertis et sauvegardés sous : '{output_fastq}'")

if __name__ == "__main__":
    export_to_fastq_v2()
