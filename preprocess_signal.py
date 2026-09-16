import pod5
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import os
import glob

class NanoporeSignalDataset(Dataset):
    def __init__(self, pod5_dir, window_size=2048, overlap=256, max_reads=100):
        self.window_size = window_size
        self.stride = window_size - overlap
        self.slices = []
        
        pod5_files = glob.glob(os.path.join(pod5_dir, "**", "*.pod5"), recursive=True)
        if not pod5_files:
            raise FileNotFoundError(f"Aucun fichier .pod5 trouve dans le dossier '{pod5_dir}'")
            
        read_count = 0
        for file_path in pod5_files:
            with pod5.Reader(file_path) as reader:
                for read_record in reader.reads():
                    raw_signal = read_record.signal.astype(np.float32)
                    
                    # 1. Normalisation Z-Score
                    mean = np.mean(raw_signal)
                    std = np.std(raw_signal)
                    if std == 0:
                        continue
                    normalized_signal = (raw_signal - mean) / std
                    
                    # 2. Fenetrage glissant (Sliding Window)
                    num_samples = len(normalized_signal)
                    for start in range(0, num_samples - window_size + 1, self.stride):
                        end = start + window_size
                        self.slices.append(normalized_signal[start:end])
                        
                    read_count += 1
                    if read_count >= max_reads:
                        break
            if read_count >= max_reads:
                break

    def __len__(self):
        return len(self.slices)

    def __getitem__(self, idx):
        # Format [1, 2048] pour correspondre a la dimension 1D-CNN (1 canal d'entree)
        return torch.tensor(self.slices[idx], dtype=torch.float32).unsqueeze(0)

if __name__ == "__main__":
    dataset = NanoporeSignalDataset(pod5_dir="real_pod5", window_size=2048, overlap=256)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    print("=== Validation du Pretraitement (Etape 2) ===")
    print(f"Nombre total de fenetres generees : {len(dataset)}")
    
    for batch_idx, signals in enumerate(dataloader):
        print(f"Forme du batch PyTorch (Batch, Canaux, Longueur) : {signals.shape}")
        print(f"Moyenne du batch : {signals.mean().item():.4f} | Ecart-type : {signals.std().item():.4f}")
        break
