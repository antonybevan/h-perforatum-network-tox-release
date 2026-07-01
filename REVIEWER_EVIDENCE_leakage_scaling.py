#!/usr/bin/env python3
"""
Leakage-control panel, global degree-matched background, and null-SD scaling.
Companion to REVIEWER_EVIDENCE.py. Run from repo root:  python REVIEWER_EVIDENCE_leakage_scaling.py
All numbers come from the committed STRING>=900 liver LCC; uses the repo's own RWR.
"""
import sys; sys.path.insert(0,'src')
import numpy as np, pandas as pd, networkx as nx
from network_tox.analysis.rwr import run_rwr
from network_tox.core.permutation import get_degree_matched_random
D='data/processed/'
G=nx.from_pandas_edgelist(pd.read_parquet(D+'network_900_liver_lcc.parquet'),'gene1','gene2')
t=pd.read_csv(D+'targets_lcc.csv')
hyp=sorted(set(t[t.compound=='Hyperforin'].gene_symbol)); quer=sorted(set(t[t.compound=='Quercetin'].gene_symbol))
dl=[g for g in pd.read_csv(D+'dili_900_lcc.csv').gene_name if g in G]; dset=set(dl)
shared=set(hyp)&set(quer)
def E(T,excl=()):
    s=run_rwr(G,T,restart_prob=0.15); ex=set(excl)
    return sum(s.get(g,0.0) for g in dl if g not in ex)
def Eself(T): return E(T,excl=T)   # leakage-controlled (exclude restart self-mass)

print("== LEAKAGE-CONTROL PANEL (STRING>=900) ==")
print("Hyp targets in DILI set (dist 0):",[x for x in hyp if x in dset])
print("Quer targets in DILI set (dist 0):",[x for x in quer if x in dset])
print(f"Baseline           : E_Hyp={E(hyp):.5f} E_Quer={E(quer):.5f} ratio={E(hyp)/E(quer):.2f}")
print(f"Self-mass excluded : E_Hyp={Eself(hyp):.5f} E_Quer={Eself(quer):.5f} ratio={Eself(hyp)/Eself(quer):.2f}")
hND=[x for x in hyp if x not in dset]; qND=[x for x in quer if x not in dset]
print(f"DILI-seeds removed : E_Hyp={E(hND):.5f} E_Quer={E(qND):.5f} ratio={E(hND)/E(qND):.2f}")
cyp_tx={'CYP3A4','CYP2C9','CYP2B6','ABCB1','ABCC2','ABCG2'}
hNoCyp=[x for x in hyp if x not in cyp_tx]
print(f"CYP/transporter out: E_Hyp={Eself(hNoCyp):.5f} E_Quer={Eself(quer):.5f} ratio={Eself(hNoCyp)/Eself(quer):.2f}  (Hyp seeds={hNoCyp})")
hNs=[x for x in hyp if x not in shared]; qNs=[x for x in quer if x not in shared]
print(f"Shared targets out : E_Hyp={Eself(hNs):.5f} E_Quer={Eself(qNs):.5f} ratio={Eself(hNs)/Eself(qNs):.2f}")

print("\n== GLOBAL DEGREE-MATCHED BACKGROUND (self-mass excluded) ==")
Eh=Eself(hyp); np.random.seed(42); null=[]
for i in range(1000):
    rt=get_degree_matched_random(G,hyp,len(hyp),seed=1000+i)
    if rt: null.append(Eself(rt))
null=np.array(null)
print(f"Hyp residual={Eh:.5f}; null mean={null.mean():.5f} 95th={np.quantile(null,.95):.5f} max={null.max():.5f}; "
      f"fold-vs-mean={Eh/null.mean():.2f}x exceeds-all={Eh>null.max()} perm-p={(np.sum(null>=Eh)+1)/(len(null)+1):.4f}")

print("\n== NULL-SD SCALING (RWR PE, random seed sets, self-mass excluded) ==")
rng=np.random.default_rng(42); allnodes=list(G.nodes()); out=[]
for n in [5,10,20,40,62]:
    vals=[Eself(list(rng.choice(allnodes,size=n,replace=False))) for _ in range(60)]
    out.append((n,np.std(vals))); print(f"  |T|={n:3d}: null SD={np.std(vals):.6f}")
ns=np.array([o[0] for o in out]); sds=np.array([o[1] for o in out])
slope,_=np.polyfit(np.log(ns),np.log(sds),1)
print(f"  log-log slope={slope:.3f}  (theoretical -0.5 for an averaged seed-set statistic)")

print("\n== SEPARATION MEASURE S_AB (Menche 2015): target set vs DILI module ==")
def closest_AB(A,B):                       # mean over a in A of min_{b in B} d(a,b)
    dB=nx.multi_source_dijkstra_path_length(G,list(B),weight=lambda u,v,d:1)
    return np.mean([dB[a] for a in A if a in dB])
def within(A):                             # mean over a in A of min_{a' in A, a'!=a} d(a,a')
    vals=[]
    for a in A:
        dd=nx.single_source_shortest_path_length(G,a)
        o=[dd[x] for x in A if x!=a and x in dd]
        if o: vals.append(min(o))
    return np.mean(vals) if vals else float('nan')
dBB=within(dl)
for nm,A in [('Hyperforin',hyp),('Quercetin',quer)]:
    dAB=0.5*(closest_AB(A,dl)+closest_AB(dl,A)); dAA=within(A)
    s=dAB-(dAA+dBB)/2.0
    print(f"  {nm:10s}: S_AB={s:+.3f}  (<d_AB>={dAB:.3f} <d_AA>={dAA:.3f} <d_BB>={dBB:.3f}) "
          f"-> {'OVERLAPPING' if s<0 else 'separated'}")
