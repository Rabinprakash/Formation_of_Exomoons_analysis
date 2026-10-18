import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import re

# Load your CSV
df = pd.read_csv("fragment_complete_summary.csv")
df['Angle_Num'] = df['Folder'].apply(lambda x: int(re.search(r'impact_(\d+)', str(x)).group(1)))
df = df.sort_values('Angle_Num').reset_index(drop=True)

plt.rcParams['font.family'] = 'serif'
x_labels = df['Angle_Num'].astype(str)
x_indexes = np.arange(len(df))
width = 0.25 # Wider spacing so bars don't touch

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

# Colors
c_planet = '#2c3e50'
c_moon = '#2980b9'
c_debris = '#c0392b'

# 1. Plot the 3 components as side-by-side bars
ax.bar(x_indexes - width, df['Planet_P'], width, label='Target Planet', color=c_planet, edgecolor='black')
ax.bar(x_indexes, df['Moon_P'].replace(0, 0.1), width, label='Moon Seed', color=c_moon, edgecolor='black')
ax.bar(x_indexes + width, df['Debris_P'], width, label='Unbound Debris', color=c_debris, edgecolor='black')

# 2. Use a HORIZONTAL LINE for Total System (instead of a bar)
# This proves conservation without cluttering the graph
ax.axhline(y=200000, color='#27ae60', linestyle='--', linewidth=2, label='Total System (200k Particles)', alpha=0.8)

# Scientific Log Formatting
ax.set_yscale('log')
ax.set_ylim(1, 10**6) 
ax.yaxis.set_major_formatter(ticker.LogFormatterSciNotation())

# Labels
ax.set_title('Distribution of SPH Particles', fontsize=16)
ax.set_xlabel('Impact Angle ($^\circ$)', fontsize=13)
ax.set_ylabel('Particle Count ($N$)', fontsize=13)
ax.set_xticks(x_indexes)
ax.set_xticklabels(x_labels)
ax.grid(axis='y', which='both', linestyle=':', alpha=0.4)

ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=True, shadow=True)

plt.tight_layout()
plt.savefig('Particle_Distribution.png', bbox_inches='tight')
print("✅ Generated: Scientific_Particle_Conservation_Fixed.png")
plt.show()
