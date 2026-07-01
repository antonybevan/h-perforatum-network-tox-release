#!/usr/bin/env python3
"""
DILI-module sensitivity (reviewer-requested robustness check).

Every other robustness test (alpha, expression floor, network threshold, degree
binning, two nulls) varies the *method*; this one varies the *disease module* --
the locus of the target--disease circularity. We remove from the 82-gene DILI
module the four genes that are simultaneously Hyperforin targets and DILI members
(ABCB1, CYP2C9, MMP2, NR1I2), giving a reduced module D' that the drug's targets
cannot directly overlap, and re-score per-target influence symmetrically for both
compounds. If the propagated advantage survives against D', it is not an artifact
of the module being defined to include the drug's own pharmacogenes.

Run from repo root:  python scripts/run_dili_module_sensitivity.py
All numbers come from the committed STRING>=900 liver LCC and the repo's own RWR.
"""
import sys; sys.path.insert(0, 'src')
import numpy as np, pandas as pd, networkx as nx
from network_tox.analysis.rwr import run_rwr
from network_tox.core.permutation import get_degree_matched_random

D = 'data/processed/'
G = nx.from_pandas_edgelist(pd.read_parquet(D + 'network_900_liver_lcc.parquet'), 'gene1', 'gene2')
t = pd.read_csv(D + 'targets_lcc.csv')
hyp = sorted(set(t[t.compound == 'Hyperforin'].gene_symbol))
quer = sorted(set(t[t.compound == 'Quercetin'].gene_symbol))
dl_full = [g for g in pd.read_csv(D + 'dili_900_lcc.csv').gene_name if g in G]
dset = set(dl_full)

overlap = [g for g in hyp if g in dset]                       # ABCB1, CYP2C9, MMP2, NR1I2
dl_red = [g for g in dl_full if g not in set(overlap)]         # reduced module D'

def E(T, module, excl=()):
    """Sum of single-seed-set RWR influence over `module`, minus genes in `excl`."""
    s = run_rwr(G, T, restart_prob=0.15); ex = set(excl)
    return sum(s.get(g, 0.0) for g in module if g not in ex)

print(f"DILI module: full |D|={len(dl_full)}  reduced |D'|={len(dl_red)}  (removed {len(overlap)}: {overlap})")
print("="*78)

# --- Propagated perturbation efficiency against each module. run_rwr already seeds
#     p0 = 1/|T|, so E is the mean per-target influence (perturbation efficiency);
#     excl=T applies the leave-one-out so neither compound is credited for restart
#     mass on its own targets. No further /|T| (that would double-normalise). ---
def propagated_E(T, module):
    return E(T, module, excl=T)

rows = []
for label, module in [('Full module D (82)', dl_full), ("Reduced module D' (78)", dl_red)]:
    eh, eq = propagated_E(hyp, module), propagated_E(quer, module)
    rows.append((label, eh, eq, eh/eq))
    print(f"{label:24s}: propagated E  Hyp={eh:.5f}  Quer={eq:.5f}  ratio={eh/eq:.2f}x")

# --- Degree-matched random-10-gene background, scored against the REDUCED module ---
print("-"*78)
eh_red = propagated_E(hyp, dl_red)
np.random.seed(42); null = []
for i in range(1000):
    rt = get_degree_matched_random(G, hyp, len(hyp), seed=1000 + i)
    if rt:
        null.append(E(rt, dl_red, excl=rt))
null = np.array(null)
p = (np.sum(null >= eh_red) + 1) / (len(null) + 1)
print(f"Reduced-module propagated background (n={len(null)}): "
      f"Hyp={eh_red:.5f}  null mean={null.mean():.5f}  95th={np.quantile(null,.95):.5f}  "
      f"max={null.max():.5f}  fold={eh_red/null.mean():.2f}x  exceeds-all={eh_red>null.max()}  perm-p={p:.4f}")

print("="*78)
print("Interpretation: ratio on D' vs D shows whether the per-target advantage is "
      "carried by\nthe entangled pharmacogenes (would collapse) or survives their removal.")

# --- persist committed result table ---
out = pd.DataFrame(
    [{'module': lab, 'n_dili_genes': len(m),
      'propagated_E_hyperforin': round(eh, 5), 'propagated_E_quercetin': round(eq, 5),
      'ratio': round(r, 3)}
     for (lab, eh, eq, r), m in zip(rows, [dl_full, dl_red])])
out.to_csv('results/tables/dili_module_sensitivity.csv', index=False)
print("\nwrote results/tables/dili_module_sensitivity.csv")
