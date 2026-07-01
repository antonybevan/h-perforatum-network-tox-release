#!/usr/bin/env python3
"""
Guney-fidelity revalidation. Reimplements Guney's canonical degree-binning
(emreg00/toolbox: get_degree_binning, pick_random_nodes_matching_selected,
calculate_closest_distance, calculate_proximity) in Python 3 and recomputes the
shortest-path proximity z-scores under three null models:
  (1) repo's +/-25% degree window, disease module fixed (the committed method);
  (2) Guney >=100-node degree binning, disease module fixed;
  (3) Guney >=100-node degree binning, two-sided (randomize targets AND disease).
Run from repo root. Network = STRING >=900 liver LCC.
"""
import sys; sys.path.insert(0,'src')
import numpy as np, pandas as pd, networkx as nx, random
D='data/processed/'
G=nx.from_pandas_edgelist(pd.read_parquet(D+'network_900_liver_lcc.parquet'),'gene1','gene2')
t=pd.read_csv(D+'targets_lcc.csv')
hyp=sorted(set(t[t.compound=='Hyperforin'].gene_symbol)); quer=sorted(set(t[t.compound=='Quercetin'].gene_symbol))
dl=[g for g in pd.read_csv(D+'dili_900_lcc.csv').gene_name if g in G]
deg=dict(G.degree()); nodes=list(G.nodes())

# ---- Guney calculate_closest_distance (faithful, vectorised via multi-source BFS) ----
_W=lambda u,v,d:1
_mind=nx.multi_source_dijkstra_path_length(G,dl,weight=_W)   # min dist from DILI module to every node
def dc_fixed(T):
    vals=[_mind[x] for x in T if x in _mind]; return np.mean(vals) if vals else np.nan

# ---- Guney get_degree_binning (>=100 per bin) ----
def get_degree_binning(g,bs=100):
    d2n={}
    for n,d in g.degree(): d2n.setdefault(d,[]).append(n)
    vals=sorted(d2n); bins=[]; i=0
    while i<len(vals):
        low=vals[i]; val=list(d2n[vals[i]])
        while len(val)<bs:
            i+=1
            if i==len(vals): break
            val.extend(d2n[vals[i]])
        if i==len(vals): i-=1
        high=vals[i]; i+=1
        if len(val)<bs and bins: l_,h_,v_=bins[-1]; bins[-1]=(l_,high,v_+val)
        else: bins.append((low,high,val))
    return bins
NB={}
for lo,hi,vs in get_degree_binning(G,100):
    for n in vs: NB[n]=vs
def guney_random(sel,rng):
    out=set()
    for s in sel:
        pool=NB[s]; ch=rng.choice(pool)
        for _ in range(20):
            if ch not in out: break
            ch=rng.choice(pool)
        out.add(ch)
    return list(out)
_pool={}
def _pool_for(d):
    if d not in _pool:
        lo,hi=int(d*0.75),int(d*1.25)+1
        _pool[d]=[n for n in nodes if lo<=deg[n]<=hi]
    return _pool[d]
def window_random(sel,rng):   # repo +/-25% (pooled for speed; same selection rule)
    out=set()
    for s in sel:
        p=_pool_for(deg[s]) or nodes; ch=rng.choice(p)
        for _ in range(20):
            if ch not in out: break
            ch=rng.choice(p)
        out.add(ch)
    return list(out)

def z_fixed(T,sampler,n=1000,seed=42):
    rng=random.Random(seed); obs=dc_fixed(T)
    null=[dc_fixed(sampler(T,rng)) for _ in range(n)]; null=[v for v in null if not np.isnan(v)]
    m,s=np.mean(null),np.std(null); return obs,m,s,((obs-m)/s if s>0 else 0.0)

_W=lambda u,v,d:1
def msbfs(S): return nx.multi_source_dijkstra_path_length(G,list(S),weight=_W)
def dc_pair_dist(T,dist):
    v=[dist[x] for x in T if x in dist]; return np.mean(v) if v else np.nan
def z_twosided_both(Th,Tq,n=1000,seed=42):
    """Two-sided null shared across compounds: one multi-source BFS per random
    disease set (size preserved). Returns (z_h, z_q)."""
    distD=msbfs(dl); oh=dc_pair_dist(Th,distD); oq=dc_pair_dist(Tq,distD)
    rng=random.Random(seed); bh=[]; bq=[]
    for _ in range(n):
        dist=msbfs(guney_random(dl,rng))
        bh.append(dc_pair_dist(guney_random(Th,rng),dist))
        bq.append(dc_pair_dist(guney_random(Tq,rng),dist))
    def z(o,nl): nl=[x for x in nl if not np.isnan(x)]; m,s=np.mean(nl),np.std(nl); return o,m,s,((o-m)/s if s>0 else 0.0)
    return z(oh,bh), z(oq,bq)

print("Observed d_c: Hyp=%.3f Quer=%.3f"%(dc_fixed(hyp),dc_fixed(quer)))
print("\n(1) repo +/-25% window, fixed disease:")
for nm,T in [('Hyperforin',hyp),('Quercetin',quer)]:
    o,m,s,z=z_fixed(T,window_random); print(f"   {nm:10s} z={z:+.2f} (obs {o:.2f}, null {m:.2f}±{s:.3f})")
print("(2) Guney >=100-bin, fixed disease:")
for nm,T in [('Hyperforin',hyp),('Quercetin',quer)]:
    o,m,s,z=z_fixed(T,guney_random); print(f"   {nm:10s} z={z:+.2f} (obs {o:.2f}, null {m:.2f}±{s:.3f})")
print("(3) Guney >=100-bin, TWO-SIDED (randomize targets AND disease, n=1000, |D*|=82):")
(oh,mh,sh,zh),(oq,mq,sq,zq)=z_twosided_both(hyp,quer,n=1000,seed=42)
print(f"   Hyperforin z={zh:+.2f} (obs {oh:.2f}, null {mh:.2f}±{sh:.3f})")
print(f"   Quercetin  z={zq:+.2f} (obs {oq:.2f}, null {mq:.2f}±{sq:.3f})")
print(f"   two-sided null SD ratio Hyp/Quer = {sh/sq:.2f} (expected sqrt(62/10)=2.49)")
