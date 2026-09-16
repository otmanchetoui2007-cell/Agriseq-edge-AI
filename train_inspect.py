import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from preprocess_signal import NanoporeSignalDataset
from model import NanoporeBasecaller

def inspect_predictions(log_probs):
    # Log_probs: [Batch, 256, 5]
    arg_maxes = torch.argmax(log_probs, dim=-1)[0] # Prend la 1ere fenetre du batch
    
    # Compter l'apparition de chaque classe (0: Blank, 1: A, 2: C, 3: G, 4: T)
    counts = {i: (arg_maxes == i).sum().item() for i in range(5)}
    mapping = {0: 'Blank', 1: 'A', 2: 'C', 3: 'G', 4: 'T'}
    summary = ", ".join([f"{mapping[k]}: {v}" for k, v in counts.items()])
    return summary

def train_pipeline():
    device = torch.device("cpu")
    dataset = NanoporeSignalDataset(pod5_dir="real_pod5", window_size=2048, overlap=256)
    dataloader = DataLoader(dataset, batch_size=5, shuffle=True)
    
    model = NanoporeBasecaller(num_classes=5).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    
    # Fixer une cible répétitive réaliste (ex: motif de 20 bases) pour stabiliser la convergence
    fixed_target = torch.tensor([[1, 2, 3, 4] * 5] * 5, dtype=torch.long) # Sequence A-C-G-T
    
    model.train()
    print("=== Verification fine de la distribution CTC ===")
    
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
                distrib = inspect_predictions(log_probs)
                print(f"[Epoch {epoch}] Loss: {loss.item():.4f} | Output distrib -> {distrib}")

if __name__ == "__main__":
    train_pipeline()
