import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from preprocess_signal import NanoporeSignalDataset
from model import NanoporeBasecaller

def ctc_decode(predictions, idx_to_char={0: '', 1: 'A', 2: 'C', 3: 'G', 4: 'T'}):
    arg_maxes = torch.argmax(predictions, dim=-1)
    decoded_sequences = []
    for b in range(arg_maxes.size(0)):
        seq = arg_maxes[b].tolist()
        collapsed = []
        previous = None
        for p in seq:
            if p != previous:
                collapsed.append(p)
                previous = p
        res = "".join([idx_to_char[p] for p in collapsed if p != 0])
        decoded_sequences.append(res)
    return decoded_sequences

def train_pipeline():
    device = torch.device("cpu")
    dataset = NanoporeSignalDataset(pod5_dir="real_pod5", window_size=2048, overlap=256)
    dataloader = DataLoader(dataset, batch_size=5, shuffle=True)
    
    model = NanoporeBasecaller(num_classes=5).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    
    # Séquence cible fixe pour la démonstration (motif A-C-G-T)
    fixed_target = torch.tensor([[1, 2, 3, 4] * 5] * 5, dtype=torch.long)
    
    model.train()
    print("=== Entraînement et Sauvegarde des Poids ===")
    
    for epoch in range(1, 6):
        for batch_idx, signals in enumerate(dataloader):
            batch_size = signals.size(0)
            optimizer.zero_grad()
            
            log_probs = model(signals)
            log_probs_ctc = log_probs.permute(1, 0, 2)
            
            input_lengths = torch.full(size=(batch_size,), fill_value=256, dtype=torch.long)
            target_lengths = torch.full(size=(batch_size,), fill_value=20, dtype=torch.long)
            
            loss = criterion(log_probs_ctc, fixed_target, input_lengths, target_lengths)
            loss.backward()
            optimizer.step()
            
            if batch_idx == 0:
                pred = ctc_decode(log_probs)[0]
                print(f"[Epoch {epoch}] Loss: {loss.item():.4f} | Décodage partiel: '{pred}'")
                
    # Sauvegarde des poids entraînés dans le fichier attendu par infer.py
    torch.save(model.state_dict(), "basecaller_weights.pth")
    print("\nPoids du modèle sauvegardés avec succès sous 'basecaller_weights.pth' !")

if __name__ == "__main__":
    train_pipeline()
