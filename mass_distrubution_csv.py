import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ============================================================
# 1. CONSTANTS
# ============================================================

# Lunar mass (kg)
M_LUNAR_KG = 7.347e22

# Initial total system mass (kg)
TOTAL_MASS_KG = 8.96e25

# Total system mass in lunar masses
TOTAL_MASS_ML = TOTAL_MASS_KG / M_LUNAR_KG

# ============================================================
# 2. LOAD EXCEL FILE
# ============================================================

df = pd.read_csv("impact_mass_summary_table.csv")

# Sort by impact angle
df = df.sort_values('Impact_Angle').reset_index(drop=True)

# ============================================================
# 3. CONVERT SCIENTIFIC STRINGS TO FLOAT
# ============================================================

# If Excel stored scientific notation as strings
for col in df.columns:
    if "kg" in col or "ML" in col:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

# ============================================================
# 4. PLOT SETTINGS
# ============================================================

plt.rcParams['font.family'] = 'serif'

x_labels = df['Impact_Angle'].astype(str)
x_indexes = np.arange(len(df))

width = 0.2

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

# ============================================================
# 5. COLORS
# ============================================================

c_planet = '#2c3e50'
c_moon = '#2980b9'
c_residual = '#c0392b'
c_escape = '#27ae60'

# ============================================================
# 6. BAR PLOTS
# ============================================================

# Planet Mass
ax.bar(
    x_indexes - 1.5 * width,
    df['Planet_Mass_ML'],
    width,
    label='Target Planet',
    color=c_planet,
    edgecolor='black'
)

# Moon Mass
ax.bar(
    x_indexes - 0.5 * width,
    df['Moon_Mass_ML'].replace(0, 1e-4),
    width,
    label='Moon Seed',
    color=c_moon,
    edgecolor='black'
)

# Residual Fragment Mass
ax.bar(
    x_indexes + 0.5 * width,
    df['Residual_Fragment_ML'].replace(0, 1e-4),
    width,
    label='Residual Fragments',
    color=c_residual,
    edgecolor='black'
)

# Escaped / Unbound Mass
ax.bar(
    x_indexes + 1.5 * width,
    df['Escaped_Mass_ML'].replace(0, 1e-4),
    width,
    label='Escaped / Unbound',
    color=c_escape,
    edgecolor='black'
)

# ============================================================
# 7. TOTAL SYSTEM REFERENCE LINE
# ============================================================

ax.axhline(
    y=TOTAL_MASS_ML,
    color='black',
    linestyle='--',
    linewidth=2,
    label=f'Total System ({TOTAL_MASS_ML:.1f} $M_L$)',
    alpha=0.8
)

# ============================================================
# 8. PRESENT-DAY MOON REFERENCE
# ============================================================

ax.axhline(
    y=1.0,
    color='gray',
    linestyle=':',
    linewidth=1.5,
    label='Present Moon (1 $M_L$)',
    alpha=0.8
)

# ============================================================
# 9. LOG SCALE
# ============================================================

ax.set_yscale('log')

ax.set_ylim(1e-3, 1e4)

ax.yaxis.set_major_formatter(
    ticker.LogFormatterSciNotation()
)

# ============================================================
# 10. LABELS & STYLE
# ============================================================

ax.set_title(
    'Mass Distribution vs. Impact Angle',
    fontsize=17,
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

ax.set_xticks(x_indexes)
ax.set_xticklabels(x_labels)

ax.grid(
    axis='y',
    which='both',
    linestyle=':',
    alpha=0.4
)

# ============================================================
# 11. LEGEND
# ============================================================

ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.02, 1),
    frameon=True,
    shadow=True,
    fontsize=11
)

# ============================================================
# 12. SAVE FIGURE
# ============================================================

plt.tight_layout()

plt.savefig(
    'Scientific_Mass_Distribution.png',
    dpi=300,
    bbox_inches='tight'
)

print("✅ Generated: Scientific_Mass_Distribution.png")

plt.show()
