import glob, os, json
from collections import defaultdict

def rev_comp(seq):
    trans = str.maketrans("ATCGN", "TAGCN")
    return seq.translate(trans)[::-1]

def read_fasta(fasta_path):
    refs = {}
    curr_name, curr_seq = None, []
    with open(fasta_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip().replace('\r', '')
            if not line:
                continue
            if line.startswith('>'):
                if curr_name:
                    refs[curr_name] = ''.join(curr_seq).upper()
                curr_name = line[1:].split()[0]
                curr_seq = []
            else:
                curr_seq.append(line)
        if curr_name:
            refs[curr_name] = ''.join(curr_seq).upper()
    return refs

def main():
    fasta_files = glob.glob("*.fasta")
    if not fasta_files:
        print("[ERREUR] Aucun fichier .fasta trouve !")
        return

    fasta_path = "fusarium_tr4_ncbi.fasta" if os.path.exists("fusarium_tr4_ncbi.fasta") else fasta_files[0]
    fastq_path = "agri_phytopathogen_reads.fastq"

    print(f"-> Base de reference : {fasta_path}")
    print(f"-> Fichier a analyser : {fastq_path}")

    refs = read_fasta(fasta_path)
    if not refs:
        print("[ERREUR] Impossible de lire le fichier FASTA.")
        return

    k = 9
    index = defaultdict(list)

    for ref_name, seq in refs.items():
        print(f"-> Reference chargee : {ref_name} ({len(seq)} bp)")
        for i in range(0, len(seq) - k + 1):
            kmer = seq[i:i+k]
            index[kmer].append(ref_name)

    print(f"-> Indexation terminee : {len(index)} k-mers uniques (k={k}).")

    total = 0
    aligned = 0
    counts = defaultdict(int)

    with open(fastq_path, 'r', encoding='utf-8', errors='ignore') as f:
        while True:
            h = f.readline()
            s = f.readline()
            p = f.readline()
            q = f.readline()
            if not q:
                break

            s = s.strip().replace('\r', '').upper()
            if not s:
                continue

            total += 1
            hit_scores = defaultdict(int)
            s_rev = rev_comp(s)

            for read_seq in (s, s_rev):
                for i in range(0, len(read_seq) - k + 1, 2):
                    kmer = read_seq[i:i+k]
                    if kmer in index:
                        for target in index[kmer]:
                            hit_scores[target] += 1

            if hit_scores:
                best_target = max(hit_scores, key=hit_scores.get)
                if hit_scores[best_target] >= 2:
                    aligned += 1
                    counts[best_target] += 1

    infection_rate = (aligned / total * 100) if total > 0 else 0.0

    print("\n" + "="*45)
    print("          RESULTATS DE DIAGNOSTIC")
    print("="*45)
    print(f"Total reads analyses     : {total}")
    print(f"Reads alignes            : {aligned}")
    print(f"Taux d'infection global  : {infection_rate:.2f}%")
    print("-" * 45)
    print("Detail par espece / cible :")
    for species, cnt in counts.items():
        print(f" -> {species}: {cnt} reads ({(cnt/total)*100:.2f}%)")
    print("="*45)

    # Export structuré pour le Jumeau Numérique et le Dashboard
    report = {
        "total_reads": total,
        "aligned_reads": aligned,
        "infection_rate": round(infection_rate, 2),
        "details": dict(counts),
        "status": "COMPLETED"
    }

    with open("rapport_diagnostic.json", "w", encoding="utf-8") as jf:
        json.dump(report, jf, indent=4, ensure_ascii=False)

    print("\n-> Rapport 'rapport_diagnostic.json' genere avec succes pour les Blocs 4 & 5.")

if __name__ == "__main__":
    main()
