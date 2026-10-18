import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import os

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Change this filename for different impact angles (e.g., "data_45deg.csv")
CSV_FILE = "hybrid_thesis_data.csv" 
OUTPUT_NAME = "Final_Orbit_Angle_Plot.png"

# Physical Constants for your system
PRIMARY_RADIUS = 1.21e7  # Rp in meters
ROCHE_FLUID = 3.2        # in Rp
ROCHE_RIGID = 2.0        # in Rp

# ==========================================
# 2. DATA EXTRACTION
# ==========================================
if not os.path.exists(CSV_FILE):
    print(f"Error: {CSV_FILE} not found. Please ensure the file is in the folder.")
else:
    df = pd.read_csv(CSV_FILE)
    last_step = df.iloc[-1] # Grabs the final state of the simulation

    # Extracting columns (with fallbacks for naming variations)
    time_h  = last_step.get('time_h', last_step.get('time', 0))
    mass_ml = last_step.get('seed_ML', last_step.get('mass_ML', 0))
    sma_rp  = last_step.get('a_rp', 0)
    ecc     = last_step.get('ecc', last_step.get('e', 0))
    # Use CSV values if they exist, otherwise calculate from SMA and ECC
    peri_rp = last_step.get('peri_rp', sma_rp * (1 - ecc))
    apo_rp  = last_step.get('apo_rp', sma_rp * (1 + ecc))

    # ==========================================
    # 3. PLOTTING
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    ax.set_facecolor('white')

    # Keplerian geometry: Planet at (0,0) means ellipse center is at -a*e
    center_x = -sma_rp * ecc
    semi_minor = sma_rp * np.sqrt(max(0, 1 - ecc**2))

    # Draw Orbit
    ax.add_patch(Ellipse((center_x, 0), width=2*sma_rp, height=2*semi_minor,
                 edgecolor='#3498db', facecolor='none', linewidth=3, 
                 label=f'Orbit Path ($e={ecc:.3f}$)', zorder=5))

    # Draw Planet
    ax.add_patch(Circle((0, 0), 1.0, color='#2d3436', fill=True, alpha=0.1, zorder=9))
    ax.add_patch(Circle((0, 0), 1.0, color='#2d3436', fill=False, linewidth=2, label='Planet (1 $R_p$)'))

    # Draw Roche Limits
    ax.add_patch(Circle((0, 0), ROCHE_FLUID, fill=False, linestyle='--', color='#d63031', label='Fluid Roche'))
    ax.add_patch(Circle((0, 0), ROCHE_RIGID, fill=False, linestyle=':', color='#fdcb6e', label='Rigid Roche'))

    # Markers
    plt.scatter(peri_rp, 0, color='#1abc9c', s=150, edgecolors='black', label=f'Periapsis ({peri_rp:.2f} $R_p$)', zorder=15)
    plt.scatter(-apo_rp, 0, color='#8e44ad', s=150, edgecolors='black', label=f'Apoapsis ({apo_rp:.2f} $R_p$)', zorder=15)

    # Metadata Box
    info_text = (f"Seed Mass: {mass_ml:.2f} $M_L$\n"
                 f"SMA: {sma_rp:.2f} $R_p$\n"
                 f"Eccentricity: {ecc:.3f}\n"
                 f"Time: {time_h:.1f} h")
    ax.text(0.05, 0.95, info_text, transform=ax.transAxes, fontsize=12, verticalalignment='top', 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#2c3e50', alpha=0.9))

    # Final Formatting
    ax.set_aspect('equal')
    limit = apo_rp * 1.15
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xlabel(r"Distance ($R_p$)", fontsize=13)
    ax.set_ylabel(r"Distance ($R_p$)", fontsize=13)
    ax.set_title("Final Stable Orbit", fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='lower right', ncol=2, framealpha=0.9, fontsize='small')
    ax.grid(True, linestyle=':', alpha=0.4)

    plt.tight_layout()
    plt.savefig(OUTPUT_NAME)
    plt.show()
    print(f"✅ Plot saved as {OUTPUT_NAME}")
