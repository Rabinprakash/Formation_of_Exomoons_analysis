import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# ============================================================
# 1. LOAD DATA
# ============================================================

CSV_FILE = "ALL_VAPOR.csv"

# Snapshot -> Hours conversion
SNAPSHOT_TO_HOUR_FACTOR = 100.0 / 3600.0

if not os.path.exists(CSV_FILE):
    print(f"❌ Error: {CSV_FILE} not found.")
    exit()

# Load CSV
df = pd.read_csv(CSV_FILE)

# Set snapshot as index
df = df.set_index('Snapshot')

# ============================================================
# 2. PREPARE DATA
# ============================================================

def get_angle(name):
    match = re.search(r'impact_(\d+)', str(name))
    return int(match.group(1)) if match else 0

# Sort columns by impact angle
sorted_cols = sorted(df.columns, key=get_angle)

df_sorted = df[sorted_cols]

# Rename columns
new_names = {
    col: f"{get_angle(col)}°"
    for col in df_sorted.columns
}

df_renamed = df_sorted.rename(columns=new_names)

# Convert snapshot number -> time in hours
df_renamed.index = (
    df_renamed.index * SNAPSHOT_TO_HOUR_FACTOR
).round(1)

# Transpose:
# Rows   -> impact angles
# Columns -> time
df_final = df_renamed.transpose()

# ============================================================
# 3. PLOTTING
# ============================================================

plt.rcParams['font.family'] = 'serif'

fig, ax = plt.subplots(
    figsize=(14, 6),
    dpi=300
)

# Heatmap
heatmap = sns.heatmap(
    df_final,

    cmap='magma',

    vmin=0.0,
    vmax=1.0,

    xticklabels=20,
    yticklabels=1,

    linewidths=0.0,

    square=False,

    cbar_kws={
        'label': r'Mean Vapor Fraction ($\delta_{vap}$)',
        'format': '%.1f'
    },

    ax=ax
)

# ============================================================
# 4. TITLES & LABELS
# ============================================================

ax.set_title(
    'Temporal Evolution of Vapor Fraction',
    fontsize=18,
    fontweight='bold',
    pad=20
)

ax.set_xlabel(
    'Time After Impact [Hours]',
    fontsize=14,
    fontweight='bold'
)

ax.set_ylabel(
    'Impact Angle [$^\\circ$]',
    fontsize=14,
    fontweight='bold'
)

# ============================================================
# 5. COLORBAR FORMATTING
# ============================================================

cbar = heatmap.collections[0].colorbar

cbar.ax.set_ylabel(
    r'Mean Vapor Fraction ($\delta_{vap}$)',
    fontsize=13,
    fontweight='bold',
    rotation=270,
    labelpad=25
)

# ============================================================
# 6. TICK STYLING
# ============================================================

ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=11)

# ============================================================
# 7. SAVE FIGURE
# ============================================================

plt.tight_layout()

plt.savefig(
    "Vapor_Heatmap.png",
    dpi=300,
    bbox_inches='tight'
)

print("✅ Vapor_Heatmap.png")

plt.show()
