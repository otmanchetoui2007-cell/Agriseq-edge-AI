import glob, os
import mappy as mp

fasta_files = glob.glob("*.fasta") + glob.glob("data_agri/*.fasta") + glob.glob("data_agri/**/*.fasta", recursive=True)
if not fasta_files:
    print("[ERREUR] Aucun fichier .fasta trouvé dans le dossier ou sous-dossiers !")
    exit(1)

fasta = fasta_files[0]
fastq = "agri_phytopathogen_reads.fastq"

if not os.path.exists(fastq):
    print(f"[ERREUR] Fichier FASTQ introuvable : {fastq}")
    exit(1)

print(f"-> Base de référence : {fasta}")
print(f"-> Fichier à analyser : {fastq}")
print("-> Alignement en cours...")

aligner = mp.Aligner(fasta, preset="map-ont")
if not aligner:
    print("[ERREUR] Échec de l'indexation du fichier FASTA.")
    exit(1)

total = 0
aligned = 0
counts = {}

with open(fastq, "r") as f:
    while True:
        h = f.readline()
        s = f.readline().strip()
        p = f.readline()
        q = f.readline()
        if not q: break

        total += 1
        hits = list(aligner.map(s))
        if hits:
            aligned += 1
            target = hits[0].ctg
            counts[target] = counts.get(target, 0) + 1

print("\n" + "="*45)
print("          RÉSULTATS DE DIAGNOSTIC")
print("="*45)
print(f"Total reads analysés     : {total}")
print(f"Reads alignés (Pathogène): {aligned}")
if total > 0:
    print(f"Taux d'infection global  : {(aligned/total)*100:.2f}%")
print("-" * 45)
print("Détail par espèce / cible :")
for species, cnt in counts.items():
    print(f" -> {species}: {cnt} reads ({(cnt/total)*100:.2f}%)")
print("="*45)
