import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import re

# ============================================================
# 1. CONSTANTS
# ============================================================

# Total system mass (kg)
TOTAL_MASS_KG = 8.96e25

# Lunar mass (kg)
M_LUNAR_KG = 7.347e22

# Total system mass in lunar masses
TOTAL_MASS_ML = TOTAL_MASS_KG / M_LUNAR_KG

# ============================================================
# 2. LOAD CSV DATA
# ============================================================

df = pd.read_csv("fragment_complete_summary.csv")

# Extract impact angle from folder names
df['Angle_Num'] = df['Folder'].apply(
    lambda x: int(re.search(r'impact_(\d+)', str(x)).group(1))
)

# Sort by impact angle
df = df.sort_values('Angle_Num').reset_index(drop=True)

# ============================================================
# 3. MASS CONVERSIONS
# ============================================================

# Planet mass in lunar masses
df['Planet_M'] = df['Planet_Mass_kg'] / M_LUNAR_KG

# Moon mass already provided in lunar masses
df['Moon_M'] = df['Moon_Mass_ML']

# Residual fragmented material
# = Total - Planet - Moon
df['Residual_M'] = (
    TOTAL_MASS_ML
    - df['Planet_M']
    - df['Moon_M']
)

# ============================================================
# 4. HANDLE ZERO VALUES FOR LOG SCALE
# ============================================================

# Log scale cannot display zero values
moon_plot = df['Moon_M'].copy()
moon_plot[moon_plot == 0] = np.nan

# ============================================================
# 5. PLOTTING SETUP
# ============================================================

plt.rcParams['font.family'] = 'serif'

x_labels = df['Angle_Num'].astype(str)
x_indexes = np.arange(len(df))

width = 0.25

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

# ============================================================
# 6. COLORS
# ============================================================

c_planet = '#2c3e50'   # Dark slate
c_moon = '#2980b9'     # Blue
c_residual = '#e74c3c' # Red

# ============================================================
# 7. BAR PLOTS
# ============================================================

# Planet mass
ax.bar(
    x_indexes - width,
    df['Planet_M'],
    width,
    label='Planet Mass',
    color=c_planet,
    edgecolor='black',
    alpha=0.9
)

# Moon mass
ax.bar(
    x_indexes,
    moon_plot,
    width,
    label='Moon Aggregate Mass',
    color=c_moon,
    edgecolor='black',
    alpha=0.9
)

# Residual fragmented material
ax.bar(
    x_indexes + width,
    df['Residual_M'],
    width,
    label='Residual Fragment Mass',
    color=c_residual,
    edgecolor='black',
    alpha=0.9
)

# ============================================================
# 8. REFERENCE LINES
# ============================================================

# Total system mass
ax.axhline(
    y=TOTAL_MASS_ML,
    color='#27ae60',
    linestyle='--',
    linewidth=2,
    label=f'Total System ({TOTAL_MASS_ML:.1f} $M_L$)',
    alpha=0.8
)

# Present-day Moon mass
ax.axhline(
    y=1.0,
    color='black',
    linestyle=':',
    linewidth=1.5,
    label='1.0 $M_L$ (Present Moon)',
    alpha=0.7
)

# ============================================================
# 9. AXIS FORMATTING
# ============================================================

# Logarithmic scale
ax.set_yscale('log')

# Axis limits
ax.set_ylim(1e-3, 1e4)

# Scientific notation formatting
ax.yaxis.set_major_formatter(
    ticker.LogFormatterSciNotation()
)

# X-axis ticks
ax.set_xticks(x_indexes)
ax.set_xticklabels(x_labels)

# ============================================================
# 10. LABELS & STYLING
# ============================================================

ax.set_title(
    'Mass Distribution vs. Impact Angle',
    fontsize=18,
    pad=20
)

ax.set_xlabel(
    'Impact Angle ($^\\circ$)',
    fontsize=14
)

ax.set_ylabel(
    'Mass [$M_L$]',
    fontsize=14
)

# Grid
ax.grid(
    axis='y',
    which='both',
    linestyle=':',
    alpha=0.4
)

# Legend
ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.02, 1),
    frameon=True,
    shadow=True,
    fontsize=11
)

# ============================================================
# 11. SAVE FIGURE
# ============================================================

plt.tight_layout()

plt.savefig(
    'Mass_Distribution.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

print("✅ Plot saved as Mass_Distribution.png")
