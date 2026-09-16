import os
import pod5
import torch
import numpy as np
import difflib
from train_real import parse_fastq
from train import ctc_decode

def evaluate_dataset_accuracy_v2(max_eval_reads=20):
    ground_truth = parse_fastq("data_agri/basecalls")
    if not ground_truth:
        print("Erreur : Aucun fichier FASTQ trouvé dans data_agri/basecalls.")
        return

    if not os.path.exists("basecaller_model.pt"):
        print("Erreur : Le fichier basecaller_model.pt est introuvable.")
        return

    model = torch.jit.load("basecaller_model.pt")
    model.eval()

    pod5_files = [os.path.join("data_agri/raw", f) for f in os.listdir("data_agri/raw") if f.endswith('.pod5')]
    
    identities = []
    evaluated = 0

    print(f"=== Évaluation V2 de la Précision ({max_eval_reads} Reads) ===")

    for p5 in pod5_files:
        try:
            with pod5.Reader(p5) as reader:
                for record in reader.reads():
                    read_id = str(record.read_id)
                    if read_id in ground_truth:
                        full_ref_seq = ground_truth[read_id]
                        raw_signal = record.signal.astype(np.float32)
                        
                        offset = 1024
                        window_size = 2048
                        
                        if len(raw_signal) < (offset + window_size) or len(full_ref_seq) < 50:
                            continue

                        # Extraction avec le même offset que l'entraînement Colab V2
                        signal_chunk = raw_signal[offset : offset + window_size]

                        mean, std = np.mean(signal_chunk), np.std(signal_chunk)
                        if std == 0: 
                            continue
                        norm_signal = (signal_chunk - mean) / std
                        
                        input_tensor = torch.tensor(norm_signal, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
                        
                        with torch.no_grad():
                            log_probs = model(input_tensor)
                        pred_seq = ctc_decode(log_probs)[0]
                        
                        # Découpage proportionnel exact de la fenêtre
                        prop_start = offset / len(raw_signal)
                        prop_end = (offset + window_size) / len(raw_signal)
                        
                        start_idx = int(len(full_ref_seq) * prop_start)
                        end_idx = int(len(full_ref_seq) * prop_end)
                        ref_subseq = full_ref_seq[start_idx:end_idx]
                        
                        if len(ref_subseq) == 0 or len(pred_seq) == 0:
                            continue

                        matcher = difflib.SequenceMatcher(None, pred_seq, ref_subseq)
                        identity = matcher.ratio() * 100
                        identities.append(identity)
                        evaluated += 1

                        if evaluated == 1:
                            print(f"\n[Exemple - Read ID: {read_id}]")
                            print(f"Prédiction  : {pred_seq}")
                            print(f"Référence   : {ref_subseq}")
                            print(f"Identité    : {identity:.2f} %\n")

                        if evaluated >= max_eval_reads:
                            break
        except Exception:
            continue
        if evaluated >= max_eval_reads:
            break

    if identities:
        avg_identity = np.mean(identities)
        print("=== Bilan de Précision V2 ===")
        print(f"Reads évalués       : {evaluated}")
        print(f"Read Identity Moyen : {avg_identity:.2f} %")
    else:
        print("Aucune correspondance valide trouvée.")

if __name__ == "__main__":
    evaluate_dataset_accuracy_v2()
