import os
import torch

def export_model():
    print("-> Chargement du modèle de Basecalling Deep Learning...")
    model_pt = "basecaller_model.pt"
    weights_v2 = "basecaller_weights_v2.pth"
    fastq_file = "agri_phytopathogen_reads.fastq"
    
    device = torch.device('cpu')
    model = None

    # 1. Tentative de chargement du modèle PyTorch complet
    if os.path.exists(model_pt):
        try:
            print(f"-> Chargement depuis : {model_pt}")
              model = torch.jit.load(model_pt, map_location=device)            
              if hasattr(model, 'eval'):
                model.eval()
            print("✅ Modèle PyTorch chargé avec succès (.pt)")
        except Exception as e:
            print(f"⚠️ Note sur {model_pt}: {e}")

    # 2. Si échec, chargement du fichier de poids V2
    if model is None and os.path.exists(weights_v2):
        try:
            from model import NanoporeBasecaller
            print(f"-> Chargement des poids V2 depuis : {weights_v2}")
            model = NanoporeBasecaller()
            model.load_state_dict(torch.load(weights_v2, map_location=device))
            model.eval()
            print("✅ Poids V2 chargés avec succès (.pth)")
        except Exception as e:
            print(f"⚠️ Note sur {weights_v2}: {e}")

    # 3. Vérification du fichier FASTQ cible
    if os.path.exists(fastq_file):
        size_mb = os.path.getsize(fastq_file) / (1024 * 1024)
        print(f"✅ Séquences FASTQ disponibles pour l'alignement : {fastq_file} ({size_mb:.2f} MB)")
    else:
        print("⚠️ Fichier FASTQ non trouvé à la racine.")

if __name__ == "__main__":
    export_model()