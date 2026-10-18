import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# =========================================================
# LOAD CSV
# =========================================================
df = pd.read_csv("angular_momentum_profiles.csv")

# =========================================================
# PLOT SETTINGS
# =========================================================
sns.set_theme(style="whitegrid")

plt.rcParams['font.family'] = 'serif'

fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

# =========================================================
# COLORS
# =========================================================
colors = {
    40: "#3498db",
    46: "#e67e22",
    52: "#9b59b6",
    56: "#2ecc71",
    60: "#e74c3c",
    65: "#000080",
    70: "#34495e"
}

# =========================================================
# SCALE ANGULAR MOMENTUM
# Divide by 1e11 for cleaner axis
# =========================================================
SCALE = 1e11

# =========================================================
# PLOT EACH IMPACT ANGLE
# =========================================================
angles = sorted(df['Angle_deg'].unique())

for angle in angles:

    sub = df[df['Angle_deg'] == angle]

    sub = sub.sort_values("Radial_Distance_Rp")

    r = sub["Radial_Distance_Rp"]

    # Scaled angular momentum
    L = sub["Median_Specific_Angular_Momentum"] / SCALE

    # Smooth curve
    L_smooth = (
        pd.Series(L)
        .rolling(window=3, center=True, min_periods=1)
        .mean()
    )

    ax.plot(
        r,
        L_smooth,
        linewidth=2.8,
        label=f"{angle}°",
        color=colors[angle]
    )

# =========================================================
# KEPLERIAN REFERENCE CURVE
# =========================================================
G = 6.674e-11
M_PLANET_EST = 8.96e25
R_PLANET = 1.2e7

r_ref = np.linspace(1.1, 8, 300)

L_kepler = np.sqrt(
    G * M_PLANET_EST * (r_ref * R_PLANET)
) / SCALE

ax.plot(
    r_ref,
    L_kepler,
    'k--',
    linewidth=3,
    label='Keplerian Circular Orbit'
)

# =========================================================
# AXIS LABELS
# =========================================================
ax.set_title(
    "Angular Momentum Distribution in Circumplanetary Disk",
    fontsize=20,
    fontweight='bold',
    pad=15
)

ax.set_xlabel(
    r"Radial Distance [$R_{planet}$]",
    fontsize=15
)

# IMPORTANT: show scaling in axis label
ax.set_ylabel(
    r"Specific Angular Momentum [$10^{11}\ m^2\,s^{-1}$]",
    fontsize=15
)

# =========================================================
# FORMATTING
# =========================================================
ax.grid(True, linestyle=':', alpha=0.5)

ax.set_xlim(1.1, 8)

ax.legend(
    title="Impact Angle",
    fontsize=11,
    title_fontsize=12,
    loc='upper left',
    frameon=True
)

# =========================================================
# SAVE
# =========================================================
plt.tight_layout()

plt.savefig(
    "angular_momentum_clean_scaled.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()

print("✅ Saved as: angular_momentum_clean_scaled.png")
