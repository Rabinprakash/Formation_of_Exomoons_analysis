import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load your data
df = pd.read_csv("hybrid_thesis_data.csv")

# 2. Set Seaborn Theme for Thesis
# 'whitegrid' is clean, 'talk' scales fonts for better readability
sns.set_theme(style="whitegrid", context="talk") 
plt.figure(figsize=(12, 7))

# 3. Filter noise so it doesn't clutter the log scale
df_plot = df.copy()
df_plot.loc[df_plot['seed_ML'] < 1e-4, 'seed_ML'] = None

# 4. Create the Plot
# Total Bound Debris
sns.lineplot(data=df_plot, x='time_h', y='total_bound_ML', 
             label="Total Bound Debris", color="#2c7fb8", linewidth=2)

# Moon Seed
sns.lineplot(data=df_plot, x='time_h', y='seed_ML', 
             label="Moon Seed", color="#d95f02", linewidth=3, linestyle="--")

# 5. Scientific Formatting
plt.yscale('log')
plt.title("Mass Evolution: 65° Giant Impact Simulation", fontsize=18, pad=20)
plt.xlabel("Time after Impact [hours]", fontsize=14)
plt.ylabel("Mass [$M_L$]", fontsize=14)

# Reference line for 1 Lunar Mass
plt.axhline(1.0, color='red', linestyle=':', alpha=0.6, label="1.0 $M_L$ Reference")

# Aesthetic tweaks
plt.legend(loc='lower right', frameon=True, shadow=True)
sns.despine() # Removes the top and right borders for a modern look

# 6. Save for Thesis
plt.tight_layout()
plt.savefig("seaborn_mass_evolution.pdf", dpi=600) # PDF is best for thesis quality
plt.show()
