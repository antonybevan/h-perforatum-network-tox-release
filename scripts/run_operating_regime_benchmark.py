#!/usr/bin/env python3
"""Operating-regime calibration benchmark for proximity-Z rank discordance.

Tests whether the effect-size/evidence dissociation documented for the
Hyperforin/Quercetin pair appears in degree-controlled random probes of the same
liver interactome -- WITHOUT modelling any toxicity outcome.

Design (audit-hardened):
  * The mechanism is the null-precision law sigma_null(|T|) ~ |T|^{-1/2}. We fit
    its exponent on the real liver LCC and compare it across the real DILI module
    and random size-matched pseudo-modules.
  * The standardized statistic Z = (d_c - mu_|T|)/sigma_|T| is a deterministic
    transform of d_c, so an *unconditional* "rank-discordance rises with R" curve
    is largely algebraic. We therefore report the empirically-contingent quantities:
      (a) the overturn-capacity envelope
            delta_max(R) = (mu_L - mu_S) + |z_S| * sigma_L * (sqrt(R) - 1),
          whose coefficients (sigma_L, mu-offset) are interactome geometry, not R;
      (b) the MARGIN-CONDITIONAL reversal rate: among degree-matched probe pairs in
          which the smaller set is genuinely closer by a material margin delta_0,
          how often does the larger set nonetheless win on standardized evidence --
          with a no-shrinkage (sigma_L := sigma_S) counterfactual;
      (c) the located position of the real Hyperforin/Quercetin pair.

Primary probes are degree-distribution-pinned to the full compound-target row
degree profile (10 Hyperforin rows + 62 Quercetin rows) using Guney (2016)
>=100-node degree bins. Candidate nodes are sampled from V\\D so distance-0 mass
cannot scale with |T|. A non-DILI-target-profile sensitivity and a
uniform-from-pool family are reported as contrasts.

Outputs (results/tables/):
  operating_regime_moments.csv   per-(mode,|T|) null mean/SD
  operating_regime_reversal.csv  reversal rates vs R (margin-conditional + no-shrink)
  operating_regime_plane.csv     probe-pair (margin, Z-gap) sample at exact R=6.2
  operating_regime_summary.csv   slopes (+CI), module-stability, delta_max, percentile

Deterministic: fixed seed 42. Run:  python scripts/run_operating_regime_benchmark.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx

PROJECT = Path(__file__).resolve().parents[1]
DATA = PROJECT / "data" / "processed"
TABLES = PROJECT / "results" / "tables"

SEED = 42
SIZES = [5, 8, 10, 15, 20, 30, 40, 60, 62, 80]
REAL_SMALL, REAL_LARGE = 10, 62          # Hyperforin / Quercetin LCC target counts
REAL_THRESHOLD = 900
REAL_SMALL_COMPOUND = "Hyperforin"
REAL_LARGE_COMPOUND = "Quercetin"
REAL_METRIC_TABLE = TABLES / "shortest_path_permutation_results.csv"
DELTAS = (0.3, 0.5)                      # pre-registered material raw-distance margins (hops)


def load_graph_module():
    edf = pd.read_parquet(DATA / "network_900_liver_lcc.parquet")
    G = nx.from_pandas_edgelist(edf, "gene1", "gene2")
    dili = sorted(set(pd.read_csv(DATA / "dili_900_lcc.csv")["gene_name"]) & set(G.nodes()))
    targets = pd.read_csv(DATA / "targets_lcc.csv")
    real_target_rows = [g for g in targets["gene_symbol"] if g in G.nodes()]
    return G, dili, real_target_rows


def load_real_pair_metrics(path=REAL_METRIC_TABLE, threshold=REAL_THRESHOLD):
    """Read the real H/Q proximity values from the canonical shortest-path table."""
    required = {"network_threshold", "compound", "n_targets", "observed_dc", "z_score"}
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} missing required columns: {sorted(missing)}")

    sub = df[df["network_threshold"] == threshold].copy()
    rows = {}
    for compound in (REAL_SMALL_COMPOUND, REAL_LARGE_COMPOUND):
        match = sub[sub["compound"] == compound]
        if len(match) != 1:
            raise ValueError(
                f"Expected exactly one {compound} row at threshold {threshold} in {path}; "
                f"found {len(match)}"
            )
        rows[compound] = match.iloc[0]

    small = rows[REAL_SMALL_COMPOUND]
    large = rows[REAL_LARGE_COMPOUND]
    out = {
        "network_threshold": int(threshold),
        "small_compound": REAL_SMALL_COMPOUND,
        "large_compound": REAL_LARGE_COMPOUND,
        "small_n": int(small["n_targets"]),
        "large_n": int(large["n_targets"]),
        "small_dc": float(small["observed_dc"]),
        "large_dc": float(large["observed_dc"]),
        "small_z": float(small["z_score"]),
        "large_z": float(large["z_score"]),
    }
    if out["small_n"] != REAL_SMALL or out["large_n"] != REAL_LARGE:
        raise ValueError(
            "Real-pair target counts in shortest-path table do not match the "
            f"operating-regime design: got {out['small_n']}/{out['large_n']}, "
            f"expected {REAL_SMALL}/{REAL_LARGE}"
        )
    return out


def dist_to_module(G, module):
    """Min shortest-path distance from every node to the nearest module gene (super-source BFS)."""
    H = G.copy()
    H.add_node("__S__")
    for m in module:
        H.add_edge("__S__", m)
    sp = nx.single_source_shortest_path_length(H, "__S__")
    return {n: v - 1 for n, v in sp.items() if n != "__S__"}


def build_pool(G, module, exclude_overlap=True):
    dm = dist_to_module(G, module)
    modset = set(module)
    pool = [n for n in G.nodes() if n in dm and (n not in modset if exclude_overlap else True)]
    didx = np.array([dm[n] for n in pool], dtype=float)
    deg = dict(G.degree())
    dg = np.array([deg[n] for n in pool])
    return pool, didx, dg


def degree_bins(dg, min_bin=100):
    """Guney-style degree bins; merge a final underfilled tail bin."""
    order = np.argsort(dg, kind="mergesort")
    bins = np.empty(len(dg), dtype=int)
    b, count, cur_deg = 0, 0, dg[order[0]]
    for idx in order:
        if dg[idx] != cur_deg:
            if count >= min_bin:
                b += 1
                count = 0
            cur_deg = dg[idx]
        bins[idx] = b
        count += 1
    if count < min_bin and b > 0:
        bins[bins == b] = b - 1
        b -= 1
    upper_edges = []
    for bid in range(b + 1):
        upper_edges.append(float(dg[bins == bid].max()))
    return bins, np.array(upper_edges, dtype=float)


def assign_degree_bins(degrees, upper_edges):
    """Assign arbitrary degrees to bins induced by the sampled candidate pool."""
    if len(upper_edges) == 0:
        raise ValueError("Cannot assign degree bins without candidate-pool edges")
    assigned = np.searchsorted(upper_edges, degrees, side="left")
    return np.clip(assigned, 0, len(upper_edges) - 1).astype(int)


def sample_dc(rng, didx, bins, members, canon_bins, m, B, mode):
    n = len(didx)
    if mode == "uniform":
        return didx[rng.integers(0, n, size=(B, m))].mean(axis=1)
    draw_bins = rng.choice(canon_bins, size=B * m)
    chosen = np.empty(B * m, dtype=int)
    for bid in np.unique(draw_bins):
        mask = draw_bins == bid
        pl = members.get(bid)
        chosen[mask] = rng.choice(pl if pl is not None and len(pl) else np.arange(n), size=mask.sum())
    return didx[chosen].reshape(B, m).mean(axis=1)


def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def fit_slope(sizes, sd_by_size):
    xs, ys = np.log(sizes), np.log([sd_by_size[m] for m in sizes])
    slope, inter = np.polyfit(xs, ys, 1)
    r2 = 1 - ((ys - (slope * xs + inter)) ** 2).sum() / ((ys - ys.mean()) ** 2).sum()
    return slope, r2


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-probes", type=int, default=20000, help="probe sets per size (committed run)")
    ap.add_argument("--n-pairs", type=int, default=500000, help="probe pairs per size-pair cell (committed run)")
    ap.add_argument("--n-boot", type=int, default=1000, help="bootstrap reps for slope CI (committed run)")
    args = ap.parse_args()
    TABLES.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)

    G, dili, real_target_rows = load_graph_module()
    real = load_real_pair_metrics()
    dili_set = set(dili)
    real_target_non_dili_rows = [t for t in real_target_rows if t not in dili_set]
    print(f"LCC nodes={G.number_of_nodes()} edges={G.number_of_edges()} "
          f"|DILI|={len(dili)} pooled-real-target-rows={len(real_target_rows)} "
          f"(unique={len(set(real_target_rows))})")

    pool, didx, dg = build_pool(G, dili, exclude_overlap=True)
    bins, bin_upper_edges = degree_bins(dg)
    members = {int(b): np.where(bins == b)[0] for b in np.unique(bins)}
    degrees = dict(G.degree())
    canon_bins = assign_degree_bins([degrees[t] for t in real_target_rows], bin_upper_edges)
    canon_bins_non_dili = assign_degree_bins([degrees[t] for t in real_target_non_dili_rows], bin_upper_edges)
    print(f"probe pool (V\\D)={len(pool)}  degree-bins={bins.max() + 1}  "
          f"canonical rows={len(canon_bins)}  non-DILI sensitivity rows={len(canon_bins_non_dili)}")

    # ---- per-size moments, primary and contrast probe families ----
    moments_rows, S_by_mode = [], {}
    mode_specs = {
        "pinned": canon_bins,
        "pinned_non_dili": canon_bins_non_dili,
        "uniform": canon_bins,
    }
    for mode, mode_bins in mode_specs.items():
        arr, sd_by = {}, {}
        for m in SIZES:
            sample_mode = "uniform" if mode == "uniform" else "pinned"
            dc = sample_dc(rng, didx, bins, members, mode_bins, m, args.n_probes, sample_mode)
            arr[m] = dc
            sd_by[m] = dc.std(ddof=0)
            moments_rows.append(dict(mode=mode, n_targets=m, mu_null=dc.mean(), sigma_null=dc.std(ddof=0)))
        S_by_mode[mode] = arr
        slope, r2 = fit_slope(SIZES, sd_by)
        # bootstrap slope CI: resample the estimated probe sample (same for both modes)
        boots = []
        for _ in range(args.n_boot):
            yy = {m: arr[m][rng.integers(0, len(arr[m]), len(arr[m]))].std(ddof=0) for m in SIZES}
            boots.append(fit_slope(SIZES, yy)[0])
        lo, hi = np.percentile(boots, [2.5, 97.5])
        print(f"[{mode}] sigma_null ~ |T|^{slope:.3f}  95%CI[{lo:.3f},{hi:.3f}]  R^2={r2:.4f}")
        if mode == "pinned":
            slope_pinned, r2_pinned, ci_pinned = slope, r2, (lo, hi)
        elif mode == "pinned_non_dili":
            slope_pinned_non_dili, r2_pinned_non_dili, ci_pinned_non_dili = slope, r2, (lo, hi)
        elif mode == "uniform":
            slope_uniform, r2_uniform, ci_uniform = slope, r2, (lo, hi)
    pd.DataFrame(moments_rows).to_csv(TABLES / "operating_regime_moments.csv", index=False)

    S = S_by_mode["pinned"]
    mu = {m: S[m].mean() for m in SIZES}
    sd = {m: S[m].std(ddof=0) for m in SIZES}
    S_non_dili = S_by_mode["pinned_non_dili"]
    mu_non_dili = {m: S_non_dili[m].mean() for m in SIZES}
    sd_non_dili = {m: S_non_dili[m].std(ddof=0) for m in SIZES}

    # ---- delta_max envelope for the real pair (exact |T_large|=62) ----
    R_real = REAL_LARGE / REAL_SMALL
    mu_offset = mu[REAL_LARGE] - mu[REAL_SMALL]
    shrink = abs(real["small_z"]) * sd[REAL_LARGE] * (np.sqrt(R_real) - 1)
    delta_max_real = mu_offset + shrink
    mu_offset_non_dili = mu_non_dili[REAL_LARGE] - mu_non_dili[REAL_SMALL]
    shrink_non_dili = abs(real["small_z"]) * sd_non_dili[REAL_LARGE] * (np.sqrt(R_real) - 1)
    delta_max_real_non_dili = mu_offset_non_dili + shrink_non_dili
    real_margin = real["large_dc"] - real["small_dc"]
    print(f"delta_max(real R=6.2)={delta_max_real:.3f}  (mu-offset={mu_offset:+.4f}, shrink={shrink:.3f}); "
          f"observed margin={real_margin:.3f} -> overturnable={real_margin < delta_max_real}")

    # ---- margin-conditional reversal vs R (base = 10) ----
    rev_rows = []
    NP = args.n_pairs
    for mL in [s for s in SIZES if s > REAL_SMALL]:
        dcS, dcL = S[REAL_SMALL], S[mL]
        si, li = rng.integers(0, len(dcS), NP), rng.integers(0, len(dcL), NP)
        aS, aL = dcS[si], dcL[li]
        ZS = (aS - mu[REAL_SMALL]) / sd[REAL_SMALL]
        ZL = (aL - mu[mL]) / sd[mL]
        ZL_ns = (aL - mu[mL]) / sd[REAL_SMALL]            # no-shrinkage counterfactual
        large_wins, small_closer = ZL < ZS, aS < aL
        row = dict(R=mL / REAL_SMALL, m_small=REAL_SMALL, m_large=mL,
                   uncond_directional_reversal=float((small_closer & large_wins).mean()),
                   uncond_rank_discord=float((small_closer == large_wins).mean()),
                   uncond_rank_concord=float((small_closer != large_wins).mean()))
        for d0 in DELTAS:
            cond = aS <= (aL - d0)
            den = int(cond.sum())
            k = int((cond & large_wins).sum())
            lo, hi = wilson(k, den)
            kk = int((cond & (ZL_ns < ZS)).sum())
            row[f"Rrev_d{d0}"] = (k / den) if den else np.nan
            row[f"Rrev_d{d0}_lo"] = lo
            row[f"Rrev_d{d0}_hi"] = hi
            row[f"Rrev_d{d0}_n"] = den
            row[f"Rrev_d{d0}_noshrink"] = (kk / den) if den else np.nan
        rev_rows.append(row)
    pd.DataFrame(rev_rows).to_csv(TABLES / "operating_regime_reversal.csv", index=False)

    # ---- operating-regime plane at exact R=6.2 (probe-pair sample) + real pair ----
    dcS, dcL = S[REAL_SMALL], S[REAL_LARGE]
    si, li = rng.integers(0, len(dcS), NP), rng.integers(0, len(dcL), NP)
    aS, aL = dcS[si], dcL[li]
    ZS = (aS - mu[REAL_SMALL]) / sd[REAL_SMALL]
    ZL = (aL - mu[REAL_LARGE]) / sd[REAL_LARGE]
    margin = aL - aS                                  # >0 : small set closer
    zgap = ZS - ZL                                    # >0 : large set stronger evidence
    sub = rng.choice(NP, size=min(3000, NP), replace=False)
    plane = pd.DataFrame(dict(margin=margin[sub], zgap=zgap[sub]))
    plane.to_csv(TABLES / "operating_regime_plane.csv", index=False)

    located_pct = float((margin < real_margin).mean() * 100)
    disc_uncond = float(((aS < aL) & (ZL < ZS)).mean())
    rank_discord_uncond = float(((aS < aL) == (ZL < ZS)).mean())
    print(f"H/Q located: margin {real_margin:.3f} at percentile={located_pct:.1f} of probe margins; "
          f"P(small closer & large stronger Z)={disc_uncond:.3f}; "
          f"rank-discordance={rank_discord_uncond:.3f}")

    # ---- module-stability of the exponent ----
    inv_rows = [dict(module="DILI(real)", n_genes=len(dili),
                     slope=fit_slope(SIZES, {m: build_module_sd(rng, G, dili, m, 2000) for m in SIZES})[0])]
    for k in range(3):
        pseudo = list(rng.choice(list(G.nodes()), size=len(dili), replace=False))
        inv_rows.append(dict(module=f"random_pseudo_{k + 1}", n_genes=len(dili),
                             slope=fit_slope(SIZES, {m: build_module_sd(rng, G, pseudo, m, 2000) for m in SIZES})[0]))
    inv = pd.DataFrame(inv_rows)
    print("exponent module-stability:\n" + inv.to_string(index=False))

    # ---- summary ----
    summary = dict(
        slope_pinned=slope_pinned, slope_pinned_lo=ci_pinned[0], slope_pinned_hi=ci_pinned[1], r2_pinned=r2_pinned,
        slope_pinned_non_dili=slope_pinned_non_dili, slope_pinned_non_dili_lo=ci_pinned_non_dili[0],
        slope_pinned_non_dili_hi=ci_pinned_non_dili[1], r2_pinned_non_dili=r2_pinned_non_dili,
        slope_uniform=slope_uniform, slope_uniform_lo=ci_uniform[0], slope_uniform_hi=ci_uniform[1], r2_uniform=r2_uniform,
        delta_max_real=delta_max_real, mu_offset_real=mu_offset, shrink_term_real=shrink,
        delta_max_real_non_dili=delta_max_real_non_dili, mu_offset_real_non_dili=mu_offset_non_dili,
        shrink_term_real_non_dili=shrink_non_dili,
        real_margin=real_margin, real_overturnable=bool(real_margin < delta_max_real),
        real_overturnable_non_dili=bool(real_margin < delta_max_real_non_dili),
        real_network_threshold=real["network_threshold"],
        real_small_compound=real["small_compound"],
        real_large_compound=real["large_compound"],
        real_n_small=real["small_n"],
        real_n_large=real["large_n"],
        real_dc_small=real["small_dc"],
        real_dc_large=real["large_dc"],
        real_z_small=real["small_z"],
        real_z_large=real["large_z"],
        real_z_gap=real["small_z"] - real["large_z"],
        located_percentile=located_pct, uncond_directional_reversal_real=disc_uncond,
        uncond_rank_discord_real=rank_discord_uncond,
        canonical_target_rows=len(real_target_rows), canonical_unique_targets=len(set(real_target_rows)),
        canonical_non_dili_target_rows=len(real_target_non_dili_rows),
        slope_DILI=float(inv.loc[0, "slope"]),
        slope_pseudo_mean=float(inv.loc[1:, "slope"].mean()),
    )
    pd.DataFrame([summary]).to_csv(TABLES / "operating_regime_summary.csv", index=False)
    print("wrote operating_regime_{moments,reversal,plane,summary}.csv to results/tables/")


def build_module_sd(rng, G, module, m, B):
    _, didx, _ = build_pool(G, module, exclude_overlap=True)
    idx = rng.integers(0, len(didx), size=(B, m))
    return didx[idx].mean(axis=1).std(ddof=0)


if __name__ == "__main__":
    main()
