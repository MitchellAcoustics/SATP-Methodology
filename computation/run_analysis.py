"""
Full four-step SATP circumplex validation pipeline.
Run from the repo root: uv run python computation/run_analysis.py
"""

import warnings
from pathlib import Path

# Initialise R session eagerly before any other imports to avoid rpy2 threading issues
import soundscapy.r_wrapper as sspyr

sspyr.get_r_session()

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import rthor
from soundscapy.satp import fit_circe, CircEResults
from circumplex import ssm_analyze
from sklearn.metrics.pairwise import cosine_similarity
from procrustes import rotational

warnings.filterwarnings("ignore", category=UserWarning)

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO = Path(__file__).parent.parent
DATA_DIR = REPO / "data"
OUTPUT_DIR = REPO / "outputs"
FIGURES_DIR = REPO / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)
FIGURES_DIR.mkdir(exist_ok=True)

scales = ["PAQ1", "PAQ2", "PAQ3", "PAQ4", "PAQ5", "PAQ6", "PAQ7", "PAQ8"]
eq_angles = [0, 45, 90, 135, 180, 225, 270, 315]

# ── Load data ─────────────────────────────────────────────────────────────────
print("Loading SATP Dataset v1.5 ...")
satp = pd.read_excel(DATA_DIR / "SATP Dataset v1.5.xlsx", na_values=["", "N/A"])
satp = satp.rename(columns={"Participant": "participant"})
satp = satp[satp["Institution"] != "LNC"].copy()
print(
    f"  {len(satp):,} rows | {satp['Language'].nunique()} languages: {sorted(satp['Language'].unique())}"
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Tracey's Circular Order Model
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Step 1: Circular Order ─────────────────────────────────────────────")
matrices = [satp[scales].dropna()]
labels = ["SATP"]
for lang in sorted(satp["Language"].unique()):
    matrices.append(satp[satp["Language"] == lang][scales].dropna())
    labels.append(lang)

rthor_results = rthor.test(matrices, order="circular8", labels=labels)
rthor_results["pass"] = (rthor_results["ci"] > 0.70) & (rthor_results["p_value"] < 0.05)

step1_df = rthor_results[rthor_results["label"] != "SATP"][
    ["label", "ci", "p_value", "pass"]
].copy()
step1_df.columns = ["language", "ci", "p_value", "pass"]
step1_df.to_csv(OUTPUT_DIR / "step1_circular_order.csv", index=False)
print(step1_df.to_string(index=False))

pass_step1 = step1_df[step1_df["pass"]]["language"].tolist()
fail_step1 = step1_df[~step1_df["pass"]]["language"].tolist()
print(f"\n  Pass ({len(pass_step1)}): {pass_step1}")
print(f"  Fail ({len(fail_step1)}): {fail_step1}")

satp_s2 = satp[satp["Language"].isin(pass_step1)].copy()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — CircE SEM
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Step 2: CircE SEM ──────────────────────────────────────────────────")
results_frames: list[CircEResults] = []
fit_errors: dict[str, Exception] = {}

for lang in sorted(satp_s2["Language"].unique()):
    lang_data = satp_s2[satp_s2["Language"] == lang].copy()
    print(f"  Fitting {lang} ...", end=" ", flush=True)
    try:
        res = fit_circe(lang_data, language=lang, datasource="SATP", errors="warn")
        results_frames.append(res)
        print("OK")
    except Exception as e:
        fit_errors[lang] = e
        print(f"ERROR: {e}")

print(
    f"\n  Completed: {len(results_frames)}/{len(satp_s2['Language'].unique())} languages"
)
for lang, err in fit_errors.items():
    print(f"  Error in {lang}: {err}")

full_table = pd.concat([r.table for r in results_frames], ignore_index=True)
full_table.to_csv(OUTPUT_DIR / "sem-fit-ipsatized.csv", index=False)
print(f"  Saved sem-fit-ipsatized.csv ({len(full_table)} rows)")

# Score equal_com model
thresholds = {"CFI": 0.92, "GFI": 0.90, "SRMR": 0.08}
sem_res = full_table.copy()
sem_res["CFI_pass"] = sem_res["cfi"] >= thresholds["CFI"]
sem_res["GFI_pass"] = sem_res["gfi"] >= thresholds["GFI"]
sem_res["SRMR_pass"] = sem_res["srmr"] < thresholds["SRMR"]
sem_res["Score"] = (
    sem_res[["CFI_pass", "GFI_pass", "SRMR_pass"]].sum(axis=1).astype(int)
)
sem_res["passing"] = pd.cut(
    sem_res["Score"], bins=[0, 3, 7], labels=["Fail", "Pass"], right=False
)

sem_scores = (
    sem_res[["language", "model", "n", "m", "cfi", "gfi", "srmr", "Score", "passing"]]
    .loc[sem_res["model"] == "equal_com"]
    .sort_values("language")
)
sem_scores.to_csv(OUTPUT_DIR / "sem-scores.csv", index=False)
print("  Saved sem-scores.csv")
print(
    sem_scores[["language", "cfi", "gfi", "srmr", "Score", "passing"]].to_string(
        index=False
    )
)

pass_step2 = (
    sem_res.loc[sem_res["model"] == "equal_com"]
    .query("passing != 'Fail'")["language"]
    .tolist()
)
fail_step2 = [l for l in pass_step1 if l not in pass_step2]
print(f"\n  Pass ({len(pass_step2)}): {pass_step2}")
print(f"  Fail ({len(fail_step2)}): {fail_step2}")

# Extract corrected angles
ang_df = sem_res[sem_res["model"] == "equal_com"][["language"] + scales].set_index(
    "language"
)
ang_df.to_csv(OUTPUT_DIR / "adjusted_angles.csv")
print("  Saved adjusted_angles.csv")
ang_dict = ang_df.T.to_dict(orient="list")

satp_s34 = satp[satp["Language"].isin(pass_step2)].copy()

# ─────────────────────────────────────────────────────────────────────────────
# STEPS 3 & 4 — SSM Location and Congruence
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Steps 3 & 4: SSM Location & Congruence ─────────────────────────────")

overall_means = (
    satp_s34.groupby("Recording")[scales]
    .mean()
    .rename(columns={s: f"{s}_ref" for s in scales})
    .reset_index()
)
ref_cols = [f"{s}_ref" for s in scales]
lang_rec_means = (
    satp_s34.groupby(["Language", "Recording"])[scales].mean().reset_index()
)


def congruence_cosine(data1, data2):
    sim = cosine_similarity(data1, data2)
    vals = np.diag(sim)
    return float(np.mean(vals)), vals


def procrustes_sim(data1, data2):
    res = rotational(data1, data2, translate=True, scale=True)
    return float(1 - res.error)


def prepare_matrices(ssm_results, target_angles=eq_angles):
    data2 = ssm_results[["x_est", "y_est"]].values
    data1 = np.column_stack(
        [
            np.cos(np.deg2rad(target_angles)),
            np.sin(np.deg2rad(target_angles)),
        ]
    )
    return data1, data2


def test_lang(lang, test_angles, target_angles=eq_angles):
    lm = lang_rec_means[lang_rec_means["Language"] == lang][
        ["Recording"] + list(scales)
    ]
    merged = lm.merge(overall_means, on="Recording")
    result = ssm_analyze(
        merged,
        scales=list(scales),
        angles=test_angles,
        measures=ref_cols,
        measures_labels=list(scales),
        boots=2000,
        seed=42,
    )
    d1, d2 = prepare_matrices(result.results, target_angles)
    cong, _ = congruence_cosine(d1, d2)
    pro = procrustes_sim(d1, d2)
    r2s = result.results["fit_est"].tolist()
    return result, cong, pro, r2s


rows = []
locating_eq = {}
locating_corr = {}

for lang in sorted(lang_rec_means["Language"].unique()):
    print(f"  SSM {lang} ...", end=" ", flush=True)
    try:
        r_eq, c_eq, p_eq, r2_eq = test_lang(lang, eq_angles)
        locating_eq[lang] = (r_eq, c_eq, p_eq, r2_eq)

        corr_ang = ang_dict.get(lang, eq_angles)
        r_corr, c_corr, p_corr, r2_corr = test_lang(lang, corr_ang)
        locating_corr[lang] = (r_corr, c_corr, p_corr, r2_corr)

        rows.append(
            {
                "Language": lang,
                "Eq Ang Cosine": round(c_eq, 4),
                "Corr Ang Cosine": round(c_corr, 4),
                "Eq Ang Procrustes": round(p_eq, 4),
                "Corr Ang Procrustes": round(p_corr, 4),
                **{f"R2_PAQ{i + 1}": round(r2_corr[i], 4) for i in range(8)},
            }
        )
        print(f"cosine(eq={c_eq:.3f}, corr={c_corr:.3f})")
    except Exception as e:
        print(f"ERROR: {e}")

congruence_df = pd.DataFrame(rows)
congruence_df.to_csv(OUTPUT_DIR / "step34_congruence.csv", index=False)
print("\n  Saved step34_congruence.csv")

# ─────────────────────────────────────────────────────────────────────────────
# Confidence Tier Classification
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Confidence Tiers ───────────────────────────────────────────────────")
all_langs = sorted(satp["Language"].unique())
tier_rows = []
for lang in all_langs:
    s1 = lang in pass_step1
    s2 = lang in pass_step2 if s1 else False
    row = congruence_df[congruence_df["Language"] == lang]
    s3_min_r2 = (
        float(row[[f"R2_PAQ{i + 1}" for i in range(8)]].min(axis=1).iloc[0])
        if not row.empty
        else None
    )
    s3 = (s3_min_r2 is not None and s3_min_r2 > 0.90) if s2 else False
    s4_cosine = float(row["Corr Ang Cosine"].iloc[0]) if not row.empty else None
    s4 = (s4_cosine is not None and s4_cosine > 0.90) if s2 else False
    # Tier definition aligned with Aletta et al. (2024):
    # Low    = fail Step 1 (circular ordering not maintained)
    # Medium = pass Step 1, fail Step 2 (quasi-circumplex not confirmed)
    #        OR pass Steps 1+2 but fail Step 3/4 (adjusted angles insufficient)
    # High   = pass all four steps
    if not s1:
        tier = "Low"
    elif not s2:
        tier = "Medium"
    elif s3 and s4:
        tier = "High"
    else:
        tier = "Medium"
    tier_rows.append(
        {
            "language": lang,
            "step1_ci": step1_df[step1_df["language"] == lang]["ci"].iloc[0]
            if lang in step1_df["language"].values
            else None,
            "step1_pass": s1,
            "step2_score": int(
                sem_scores[sem_scores["language"] == lang]["Score"].iloc[0]
            )
            if lang in sem_scores["language"].values
            else None,
            "step2_pass": s2,
            "step3_min_r2": s3_min_r2,
            "step3_pass": s3,
            "step4_cosine": s4_cosine,
            "step4_procrustes": float(row["Corr Ang Procrustes"].iloc[0])
            if not row.empty
            else None,
            "step4_pass": s4,
            "tier": tier,
        }
    )

tiers_df = pd.DataFrame(tier_rows)
tiers_df.to_csv(OUTPUT_DIR / "confidence_tiers.csv", index=False)
print(tiers_df[["language", "tier"]].to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────────
# Figures
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Figures ────────────────────────────────────────────────────────────")

if "cmn" in locating_eq:
    fig = locating_eq["cmn"][0].plot_circle(
        angle_labels=list(scales), title="Mandarin — equal angles"
    )
    plt.savefig(FIGURES_DIR / "cmn_eq_angles.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved cmn_eq_angles.png")

if "cmn" in locating_corr:
    fig = locating_corr["cmn"][0].plot_circle(
        angle_labels=list(scales), title="Mandarin — corrected angles"
    )
    plt.savefig(FIGURES_DIR / "cmn_corr_angles.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved cmn_corr_angles.png")

# W06 cross-language scatter with adjusted angles
high_langs = tiers_df[tiers_df["tier"] == "High"]["language"].tolist()
if high_langs:
    import soundscapy as sspy

    def adj_iso_pl(values, angles, scale=100):
        num = sum(np.cos(np.deg2rad(a)) * v for a, v in zip(angles, values))
        denom = scale / 2 * sum(abs(np.cos(np.deg2rad(a))) for a in angles)
        return num / denom

    def adj_iso_ev(values, angles, scale=100):
        num = sum(np.sin(np.deg2rad(a)) * v for a, v in zip(angles, values))
        denom = scale / 2 * sum(abs(np.sin(np.deg2rad(a))) for a in angles)
        return num / denom

    w06 = satp.query("Recording == 'W06' and Language in @high_langs")
    res_rows = []
    for lang in high_langs:
        ld = w06[w06["Language"] == lang]
        if ld.empty:
            continue
        ang = ang_dict.get(lang, eq_angles)
        pl = ld.apply(lambda r: adj_iso_pl(r[scales].values, ang), axis=1).mean()
        ev = ld.apply(lambda r: adj_iso_ev(r[scales].values, ang), axis=1).mean()
        res_rows.append({"Language": lang, "ISOPleasant": pl, "ISOEventful": ev})

    if res_rows:
        w06_df = pd.DataFrame(res_rows)
        fig, ax = plt.subplots(figsize=(7, 7))
        sspy.plotting.scatter(
            w06_df, hue="Language", s=80, title="W06 — adjusted angles", ax=ax
        )
        plt.savefig(FIGURES_DIR / "W06_comparison.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("  Saved W06_comparison.png")

print("\n✓ Analysis complete. All outputs saved.")
