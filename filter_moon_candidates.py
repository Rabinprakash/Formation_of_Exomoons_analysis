#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg') 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import re

# ==========================================================
# 1. SETUP & CONSTANTS
# ==========================================================
DATA_DIR = "./" 
OUT_DIR = "./FINAL_THESIS_ANALYSIS"
os.makedirs(OUT_DIR, exist_ok=True)

G = 6.67430e-11
M_MOON = 7.347e22
R_PLANET = 1.21e7
R_ROCHE = 3.89e7
SPH_TIMESTEP = 100.0
STAR_MASS = 1.99e30
PLANET_A = 1.496e11
HILL_FRACTION = 0.7

# ==========================================================
# 2. CORE ENGINE
# ==========================================================
def run_hybrid_analysis():
    agg_files = sorted(glob.glob(os.path.join(DATA_DIR, "impact.*_fragments_aggregates.txt")))
    results = []

    print(f"🚀 Processing {len(agg_files)} snapshots for Mass and Orbit...")

    for fpath in agg_files:
        try:
            # Extract Time
            step_match = re.search(r"impact\.(\d+)", fpath)
            if not step_match: continue
            step = int(step_match.group(1))
            time_h = (step * SPH_TIMESTEP) / 3600.0

            # 1. Get Moon Seed Mass from Aggregates file
            seed_mass_kg = 0.0
            with open(fpath, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if "# 2nd-largest aggregate:" in line:
                        data = lines[i+2].replace('#', '').strip().split()
                        seed_mass_kg = abs(float(data[0]))
                        break

            # 2. Get Physics and Bound Debris from Fragments file
            out_path = fpath.replace("_aggregates.txt", ".out")
            if not os.path.exists(out_path): continue
            
            # Using engine='c' for speed
            df = pd.read_csv(out_path, sep=r"\s+", comment="#", header=None, engine='c')
            
            # Identify Primary Planet (Body with max mass)
            idx_p = df[6].idxmax()
            mp = df.loc[idx_p, 6]
            r_p = df.loc[idx_p, [0,1,2]].values
            v_p = df.loc[idx_p, [3,4,5]].values

            # Vectorized calculations for ALL fragments
            r_rel_all = df[[0,1,2]].values - r_p
            v_rel_all = df[[3,4,5]].values - v_p
            r_mag_all = np.linalg.norm(r_rel_all, axis=1)
            v_mag_all = np.linalg.norm(v_rel_all, axis=1)
            
            mu_all = G * (mp + df[6].abs().values)
            energy_all = 0.5 * v_mag_all**2 - mu_all / np.where(r_mag_all==0, np.inf, r_mag_all)
            
            # Calculate Hill Sphere for this step
            r_hill = PLANET_A * (mp / (3 * STAR_MASS))**(1/3) * HILL_FRACTION
            
            # Define Bound Debris: E < 0, outside Roche, inside Hill, not the planet
            bound_mask = (energy_all < 0) & (r_mag_all > R_ROCHE) & (r_mag_all < r_hill) & (df.index != idx_p)
            total_bound_kg = df.loc[bound_mask, 6].abs().sum()

            # 3. Calculate Moon Seed Orbit
            a, ecc, rp, ra = np.nan, np.nan, np.nan, np.nan
            
            if seed_mass_kg > 1e21: # Ensure it's a real clump, not noise
                # Find the row in .out that matches the seed mass
                seed_idx = (df[6].abs() - seed_mass_kg).abs().idxmin()
                
                dist = r_mag_all[seed_idx]
                vel = v_mag_all[seed_idx]
                mu_seed = G * (mp + seed_mass_kg)
                energy_seed = 0.5 * vel**2 - mu_seed / dist
                
                if energy_seed < 0:
                    a = -mu_seed / (2 * energy_seed)
                    h_vec = np.cross(r_rel_all[seed_idx], v_rel_all[seed_idx])
                    h_mag = np.linalg.norm(h_vec)
                    e2 = 1 + (2 * energy_seed * h_mag**2) / mu_seed**2
                    ecc = np.sqrt(max(0, e2))
                    rp, ra = a*(1-ecc), a*(1+ecc)

            results.append({
                "time_h": time_h,
                "seed_ML": seed_mass_kg / M_MOON,
                "total_bound_ML": total_bound_kg / M_MOON,
                "a_rp": a / R_PLANET,
                "ecc": ecc,
                "peri_rp": rp / R_PLANET,
                "apo_rp": ra / R_PLANET
            })

        except Exception as e:
            print(f"Error at {fpath}: {e}")
            continue

    return pd.DataFrame(results)

# ==========================================================
# 3. RUN, SAVE & PLOT
# ==========================================================
df_final = run_hybrid_analysis().sort_values("time_h")
df_final = df_final.ffill() # Clean up last-step glitches

# Save data
csv_path = os.path.join(OUT_DIR, "hybrid_thesis_data.csv")
df_final.to_csv(csv_path, index=False)

# Plotting
plt.style.use('bmh')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Top: Mass Evolution
ax1.plot(df_final['time_h'], df_final['total_bound_ML'], label="Total Bound Debris", color='navy', alpha=0.6)
ax1.plot(df_final['time_h'], df_final['seed_ML'], label="Moon Seed (2nd Aggregate)", color='darkorange', lw=2)
ax1.set_yscale('log')
ax1.set_ylabel("Mass [$M_L$]")
ax1.legend()
ax1.set_title("Mass Evolution and Orbital Stability:60")

# Bottom: Orbital Stability
# Filter out the 10^-23 noise for a cleaner plot
df_orbit = df_final[df_final['seed_ML'] > 0.1] 
ax2.plot(df_orbit['time_h'], df_orbit['a_rp'], color='black', label="Semi-major Axis")
ax2.fill_between(df_orbit['time_h'], df_orbit['peri_rp'], df_orbit['apo_rp'], color='teal', alpha=0.3, label="Orbital Range")
ax2.axhline(R_ROCHE/R_PLANET, color='red', ls='--', label="Roche Limit")
ax2.set_ylabel("Distance [$R_p$]")
ax2.set_xlabel("Time [hours]")
ax2.set_ylim(0, 50)
ax2.legend()

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "Thesis_Double_Plot.png"))
print(f"✅ Success! Data and Double Plot saved in {OUT_DIR}")
