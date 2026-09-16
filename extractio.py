# Script d'extraction et de tracé ROC (donnees_roc.csv)
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Charger vos données expérimentales réelles (Colonnes: 'ground_truth', 'hit_count')
df = pd.read_csv("donnees_roc_reelles.csv") 

fpr, tpr, thresholds = roc_curve(df['ground_truth'], df['hit_count'])
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 5), dpi=300)
plt.plot(fpr, tpr, color='#0284c7', lw=2, label=f'AgriSeq k-9 (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.xlabel('Taux de Faux Positifs (1 - Spécificité)')
plt.ylabel('Taux de Vrais Positifs (Sensibilité)')
plt.title('Courbe ROC Réelle — Alignement k-mers (TR4)')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
plt.savefig("courbe_roc_reelle.pdf", bbox_inches='tight')