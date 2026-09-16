import os
import pod5
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader
from model import NanoporeBasecaller
from train import ctc_decode

BASE_MAP = {'A': 1, 'C': 2, 'G': 3, 'T': 4}

def parse_fastq(fastq_dir):
    reads = {}
    fastq_files = [os.path.join(fastq_dir, f) for f in os.listdir(fastq_dir) if f.endswith('.fastq')]
    for fq in fastq_files:
        with open(fq, 'r', encoding='utf-8', errors='ignore') as f:
            while True:
                header = f.readline()
                if not header: break
                seq = f.readline().strip().upper()
                f.readline()
                f.readline()
                read_id = header.split()[0][1:]
                reads[read_id] = seq
    return reads

class RealNanoporeDataset(Dataset):
    def __init__(self, pod5_dir, fastq_dir, window_size=2048, max_samples=3000):
        self.samples = []
        self.window_size = window_size
        ground_truth = parse_fastq(fastq_dir)
        
        pod5_files = [os.path.join(pod5_dir, f) for f in os.listdir(pod5_dir) if f.endswith('.pod5')]
        
        for p5 in pod5_files:
            try:
                with pod5.Reader(p5) as reader:
                    for record in reader.reads():
                        read_id = str(record.read_id)
                        if read_id in ground_truth:
                            raw_signal = record.signal.astype(np.float32)
                            seq = ground_truth[read_id]
                            
                            if len(raw_signal) < window_size or len(seq) < 20:
                                continue
                                
                            # Normalisation Z-Score du signal
                            mean, std = np.mean(raw_signal), np.std(raw_signal)
                            if std == 0: continue
                            norm_signal = (raw_signal - mean) / std
                            
                            # Extraction de la première fenêtre de 2048 points
                            window = norm_signal[:window_size]
                            
                            # Découpage proportionnel de la séquence vraie pour la fenêtre
                            prop = window_size / len(raw_signal)
                            target_len = max(5, int(len(seq) * prop))
                            target_seq = seq[:target_len]
                            
                            # Conversion A, C, G, T en identifiants 1, 2, 3, 4
                            target_indices = [BASE_MAP[b] for b in target_seq if b in BASE_MAP]
                            
                            if len(target_indices) > 0:
                                self.samples.append((
                                    torch.tensor(window, dtype=torch.float32).unsqueeze(0),
                                    torch.tensor(target_indices, dtype=torch.long)
                                ))
                            
                            if len(self.samples) >= max_samples:
                                break
            except Exception:
                continue
            if len(self.samples) >= max_samples:
                break
                
    def __len__(self):
        return len(self.samples)
        
    def __getitem__(self, idx):
        return self.samples[idx]

def collate_fn(batch):
    signals = torch.stack([item[0] for item in batch])
    targets = [item[1] for item in batch]
    target_lengths = torch.tensor([len(t) for t in targets], dtype=torch.long)
    
    max_len = max(target_lengths)
    padded_targets = torch.zeros(len(batch), max_len, dtype=torch.long)
    for i, t in enumerate(targets):
        padded_targets[i, :len(t)] = t
        
    return signals, padded_targets, target_lengths

def train_real():
    dataset = RealNanoporeDataset(pod5_dir="data_agri/raw", fastq_dir="data_agri/basecalls", max_samples=2000)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True, collate_fn=collate_fn)
    
    device = torch.device("cpu")
    model = NanoporeBasecaller(num_classes=5).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    
    print(f"=== Entraînement Réel sur {len(dataset)} Échantillons Fongiques ===")
    model.train()
    
    for epoch in range(1, 6):
        total_loss = 0
        for batch_idx, (signals, targets, target_lengths) in enumerate(dataloader):
            batch_size = signals.size(0)
            optimizer.zero_grad()
            
            log_probs = model(signals) # [Batch, 256, 5]
            log_probs_ctc = log_probs.permute(1, 0, 2) # [256, Batch, 5]
            
            input_lengths = torch.full(size=(batch_size,), fill_value=256, dtype=torch.long)
            
            loss = criterion(log_probs_ctc, targets, input_lengths, target_lengths)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx == 0:
                pred = ctc_decode(log_probs)[0]
                print(f"[Epoch {epoch}] Batch Loss: {loss.item():.4f} | Séquence prédite : '{pred}'")
                
        avg_loss = total_loss / len(dataloader)
        print(f"--> Fin Epoch {epoch} | Loss Moyenne : {avg_loss:.4f}\n")
        
    torch.save(model.state_dict(), "basecaller_weights.pth")
    print("Nouveaux poids entraînés sauvegardés sous 'basecaller_weights.pth' !")

if __name__ == "__main__":
    train_real()
