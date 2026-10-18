# Formation of Exomoons Analysis

A data analysis and simulation project studying giant-impact moon formation outcomes across different impact angles.

## Overview

This repository contains the dataset, analysis scripts, and plotting code used to evaluate how impact angle influences:

- the formation of moon seeds,
- vaporization and debris production,
- particle fate distributions,
- orbital stability and angular momentum structure,
- and final mass partition across planet, moon, residual debris, and escaped material.

The project is organized around a parameter sweep over impact angles approximately spanning 40°, 46°, 52°, 56°, 60°, 65°, and 70°.

## Repository Contents

- `ALL_VAPOR.csv` — mean vapor fraction time series for each impact case.
- `angular_momentum.py` — generates angular momentum vs. radial distance plots.
- `angular_momentum_profiles.csv` — radial angular momentum profile data by impact angle.
- `fragment_complete_summary.csv` — final summary of planet, moon, and debris particle counts and masses.
- `impact_mass_summary_table.csv` — mass summary in both SI units and lunar masses.
- `particle_number_summary.csv` — particle counts by fate: planet, moon, residual, escaped.
- `filter_moon_candidates.py` — hybrid analysis script for moon seed and orbit stability assessment.
- `mass_evolution.py` — mass evolution plotting over time.
- `orbit.py` — final orbit visualization script.
- `heat_map.py` — vapor fraction heatmap generation.
- `mass_impact.py` and `mass_distrubution_csv.py` — mass-distribution plots.
- `particle.py` and `particle_number_csv.py` — particle-distribution plots.
- `convert_xdmf.py` — utility to convert HDF5 output to XDMF for visualization tools.
- `hybrid_thesis_data.csv` — generated output for hybrid mass/orbit analysis.

## Project Goal

The primary objective is to quantify which impact angles produce a viable moon-forming disk and which conditions favor:

- stable moon seed accretion,
- high vaporization,
- significant escape of material,
- or failure to form a bound moon candidate.

## Data Interpretation

From the dataset, the strongest moon-seed outcomes appear at intermediate-to-high impact angles, especially near 56°–70°, with the largest moon mass candidates emerging around 65° in the summary tables. Lower-angle cases produce little or no bound moon seed mass.

Key signal dimensions include:

- vapor fraction evolution over time,
- total bound debris mass,
- moon seed mass in lunar masses,
- residual fragment mass,
- escaped/unbound mass,
- orbital semi-major axis and eccentricity.

## Dependencies

This project is primarily Python-based and requires packages such as:

- pandas
- numpy
- matplotlib
- seaborn
- h5py (for XDMF conversion utility)

Install dependencies with:

```bash
pip install pandas numpy matplotlib seaborn h5py
```

## Usage

Run the plotting scripts directly from the project root:

```bash
python heat_map.py
python angular_momentum.py
python mass_impact.py
python particle.py
python orbit.py
```

For the hybrid analysis workflow:

```bash
python filter_moon_candidates.py
```

This generates the hybrid dataset and associated plots in the `FINAL_THESIS_ANALYSIS/` directory when applicable.

## Expected Outputs

Typical outputs include:

- vapor heatmap figure,
- angular momentum profile plot,
- mass distribution plots,
- particle distribution plots,
- final orbit plot,
- hybrid mass evolution and orbital stability figures.

## Notes

This repository is intended for research, analysis, and thesis-style visualization. Some scripts are exploratory and may require file-path or naming alignment depending on the local working directory.

## License

This project is shared for academic and research use.

## Contact

For questions or collaboration, please contact the project maintainer.
