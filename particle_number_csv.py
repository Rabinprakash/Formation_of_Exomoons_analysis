import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ============================================================
# 1. LOAD EXCEL FILE
# ============================================================

df = pd.read_csv("particle_number_summary.csv")

# Sort by impact angle
df = df.sort_values('Impact_Angle').reset_index(drop=True)

# ============================================================
# 2. PLOT SETTINGS
# ============================================================

plt.rcParams['font.family'] = 'serif'

x_labels = df['Impact_Angle'].astype(str)
x_indexes = np.arange(len(df))

width = 0.2

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

# ============================================================
# 3. COLORS
# ============================================================

c_planet = '#2c3e50'
c_moon = '#2980b9'
c_residual = '#c0392b'
c_escape = '#27ae60'

# ============================================================
# 4. PLOT BARS
# ============================================================

# Planet particles
ax.bar(
    x_indexes - 1.5 * width,
    df['Planet_Particles'],
    width,
    label='Target Planet',
    color=c_planet,
    edgecolor='black'
)

# Moon particles
ax.bar(
    x_indexes - 0.5 * width,
    df['Moon_Particles'].replace(0, 0.1),
    width,
    label='Moon Seed',
    color=c_moon,
    edgecolor='black'
)

# Residual fragments
ax.bar(
    x_indexes + 0.5 * width,
    df['Residual_Particles'].replace(0, 0.1),
    width,
    label='Residual Fragments',
    color=c_residual,
    edgecolor='black'
)

# Escaped particles
ax.bar(
    x_indexes + 1.5 * width,
    df['Escaped_Particles'].replace(0, 0.1),
    width,
    label='Escaped / Unbound',
    color=c_escape,
    edgecolor='black'
)

# ============================================================
# 5. TOTAL PARTICLE REFERENCE LINE
# ============================================================

ax.axhline(
    y=200000,
    color='black',
    linestyle='--',
    linewidth=2,
    label='Total System (200k Particles)',
    alpha=0.8
)

# ============================================================
# 6. LOG SCALE
# ============================================================

ax.set_yscale('log')

ax.set_ylim(1, 1e6)

ax.yaxis.set_major_formatter(
    ticker.LogFormatterSciNotation()
)

# ============================================================
# 7. LABELS & STYLING
# ============================================================

ax.set_title(
    'Distribution of SPH Particles vs. Impact Angle',
    fontsize=17,
    pad=20
)

ax.set_xlabel(
    'Impact Angle ($^\\circ$)',
    fontsize=14
)

ax.set_ylabel(
    'Particle Count ($N$)',
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
# 8. LEGEND
# ============================================================

ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.02, 1),
    frameon=True,
    shadow=True,
    fontsize=11
)

# ============================================================
# 9. SAVE FIGURE
# ============================================================

plt.tight_layout()

plt.savefig(
    'Scientific_Particle_Distribution.png',
    dpi=300,
    bbox_inches='tight'
)

print("✅ Generated: Scientific_Particle_Distribution.png")

plt.show()
