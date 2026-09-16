import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuration du style scientifique
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 8

fig = plt.figure(figsize=(10, 8), dpi=300)
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25)

# -------------------------------------------------------------------
# PANNEAU A : Télédétection Satellite & Détection d'Anomalie (NDVI)
# -------------------------------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])
np.random.seed(42)
ndvi = np.random.uniform(0.55, 0.85, (50, 50))
y, x = np.ogrid[:50, :50]
mask = (x - 25)**2 + (y - 25)**2 <= 8**2
ndvi[mask] = np.random.uniform(0.18, 0.32, np.count_nonzero(mask))

im1 = ax1.imshow(ndvi, cmap='YlGn', vmin=0, vmax=1)
circle = patches.Circle((25, 25), 9, edgecolor='red', facecolor='none', lw=1.5, ls='--')
ax1.add_patch(circle)
ax1.set_title("(A) Télédétection Satellite (Sentinel-2 NDVI)", fontweight='bold', loc='left')
ax1.axis('off')
cbar1 = fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
cbar1.set_label('Indice NDVI', fontsize=7)
ax1.text(25, 10, "Foyer TR4\nNDVI < 0.3", color='red', fontsize=7, ha='center', fontweight='bold')

# -------------------------------------------------------------------
# PANNEAU B : Deep Learning Basecalling (Signal pA -> Fastq)
# -------------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])
time = np.linspace(0, 10, 200)
signal = np.sin(time*3) + np.random.normal(0, 0.2, 200) + 2
ax2.plot(time, signal, color='#1f77b4', lw=0.8, label='Signal brut (pA)')
ax2.set_title("(B) Edge Basecalling PyTorch (CRNN + CTC)", fontweight='bold', loc='left')
ax2.set_xlabel('Temps (ms)', fontsize=7)
ax2.set_ylabel('Courant (pA)', fontsize=7)
ax2.grid(True, linestyle=':', alpha=0.6)

# Overlay de la séquence prédite
bases = ['A', 'C', 'G', 'T', 'T', 'A', 'G', 'C']
pos = np.linspace(1, 9, len(bases))
for p, b in zip(pos, bases):
    ax2.text(p, 4.2, b, fontsize=8, fontweight='bold', color='#d62728', ha='center')
ax2.set_ylim(0, 5)

# -------------------------------------------------------------------
# PANNEAU C : Alignement Genomique k-mers & Quantification
# -------------------------------------------------------------------
ax3 = fig.add_subplot(gs[1, 0])
categories = ['Reads Cibles (TR4)', 'ADN Hôte / Non-aligné']
counts = [7797, 62418]
colors = ['#d62728', '#2ca02c']

wedges, texts, autotexts = ax3.pie(counts, labels=categories, autopct='%1.1f%%',
                                  startangle=140, colors=colors, 
                                  textprops=dict(fontsize=7),
                                  explode=(0.1, 0))
plt.setp(autotexts, size=8, weight="bold", color="white")
ax3.set_title("(C) Identification Génétique (NCBI AY520188.1)", fontweight='bold', loc='left')

# -------------------------------------------------------------------
# PANNEAU D : Vectorisation KML & Pulvérisation Ciblé par Drone
# -------------------------------------------------------------------
ax4 = fig.add_subplot(gs[1, 1])
# Trajectoire Drone
drone_x = [10, 10, 20, 20, 30, 30, 40, 40]
drone_y = [10, 40, 40, 10, 10, 40, 40, 10]
ax4.plot(drone_x, drone_y, color='#7f7f7f', ls=':', label='Plan de vol (.KML)')
ax4.scatter([25], [25], color='red', s=300, alpha=0.3, label='Zone de pulvérisation')
ax4.scatter([25], [25], color='red', s=50, marker='x')

ax4.set_title("(D) Intervention Robotisée Ciblée (Drone)", fontweight='bold', loc='left')
ax4.set_xlabel('Coordonnées Longitude (m)', fontsize=7)
ax4.set_ylabel('Coordonnées Latitude (m)', fontsize=7)
ax4.legend(loc='lower right', fontsize=6)
ax4.grid(True, linestyle=':', alpha=0.6)

# Sauvegarde de la figure haute résolution
plt.tight_layout()
plt.savefig("figure_recherche_agriseq.png", dpi=300, bbox_inches='tight')
plt.show()