# 🛰️ SBDB Orbital Cluster Analyzer

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A powerful Python-based toolkit for fetching, processing, clustering, and visualizing orbital data from NASA’s **Small-Body Database (SBDB)**.  
Developed by **Steven M Tilley** ([@steveareno225](https://github.com/steveareno225)), this open-source project leverages AI-enhanced coding (via ChatGPT / Cody) and is intended as a research-grade starting point.

---

## 📌 Features

- 📡 Fetch millions of objects from the [SBDB API](https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html)
- 📊 Compute orbital dissimilarity (`D_SH`) metrics
- 🔗 Identify clusters of objects with similar orbits
- 🖼 Generate histograms and scatter plots for orbital dynamics
- 🧪 Filter for close-matching object pairs at multiple thresholds

---

## 🚀 Quick Start

### ⚙️ Requirements

- Python 3.9+
- Libraries: `pandas`, `matplotlib`, `requests`

Install dependencies:
```bash
pip install -r requirements.txt
```

### 🧰 Run the Full Pipeline (Windows)

Use the included batch file:
```bat
sbdb.bat
```

Or run manually:
```bash
python sbdb_fetcher.py
python D_SH_Processing.py
python generate_cluster_report.py
python Plot_Generator.py
```

---

## 🧠 How It Works

| Script | Role |
|--------|------|
| `sbdb_fetcher.py` | Fetches the full SBDB catalog (1.4M+ objects) with precision orbital data |
| `D_SH_Processing.py` | Calculates D_SH dissimilarity scores and exports filtered subsets |
| `generate_cluster_report.py` | Groups objects into clusters based on orbital similarity |
| `Plot_Generator.py` | Visualizes histograms and scatter plots by object type (e.g. comet vs asteroid) |

---

## 📁 Output Data

The scripts produce structured CSV outputs:

| File | Description |
|------|-------------|
| `sbdb_query_results.csv` | Raw fetched orbital dataset |
| `SBDB_sorted_DSH.csv` | Dataset sorted with D_SH dissimilarity values |
| `D_SH_filtered_below_*.csv` | Subsets filtered by D_SH threshold (0.01 to 1.00) |
| `Filtered_Clusters_2plus.csv` | Groupings of related small bodies (2+ linked) |

Plots are saved to:

```
/orbital_plots/
    ├── D_SH_distribution.png
    ├── a_distribution.png
    ├── e_distribution.png
    ├── ...
    └── /scatter/
          ├── Asteroids_q_vs_a.png
          ├── Comets_i_vs_e.png
          └── ...
```

---

## 🧪 Research Use

This tool supports planetary defense, small-body dynamics, and solar system formation studies.  
Users can adjust thresholds, clustering logic, or add new filters to support their mission.

---

## 📄 License

MIT License – see [`LICENSE`](LICENSE) for full terms.

---

## 🙌 Contributing

Issues, forks, and pull requests welcome!

---

> Made with 💻 by Steven M Tilley | Powered by Python + NASA SBDB + AI 👾
