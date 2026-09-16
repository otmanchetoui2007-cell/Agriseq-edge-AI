from train_real import RealNanoporeDataset, collate_fn
from model import NanoporeBasecaller
from train import ctc_decode
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

def train_scaleup():
    print("Chargement du jeu de données étendu (50 000 échantillons)...")
    dataset = RealNanoporeDataset(
        pod5_dir="data_agri/raw", 
        fastq_dir="data_agri/basecalls", 
        max_samples=50000
    )
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, collate_fn=collate_fn)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Entraînement sur matériel : {device}")
    
    model = NanoporeBasecaller(num_classes=5).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=5e-4)
    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    
    epochs = 20
    print(f"=== Début de l'Entraînement Échelle Réelle ({epochs} Epochs) ===")
    
    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0
        for signals, targets, target_lengths in dataloader:
            signals = signals.to(device)
            targets = targets.to(device)
            target_lengths = target_lengths.to(device)
            
            optimizer.zero_grad()
            log_probs = model(signals)
            log_probs_ctc = log_probs.permute(1, 0, 2)
            input_lengths = torch.full(size=(signals.size(0),), fill_value=256, dtype=torch.long, device=device)
            
            loss = criterion(log_probs_ctc, targets, input_lengths, target_lengths)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch [{epoch}/{epochs}] - Loss Moyenne : {avg_loss:.4f}")
        
        if epoch % 5 == 0 or epoch == epochs:
            torch.save(model.state_dict(), "basecaller_weights.pth")
            print(f"--> Poids sauvegardés (Epoch {epoch})")

if __name__ == "__main__":
    train_scaleup()
