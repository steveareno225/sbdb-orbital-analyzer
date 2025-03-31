import pandas as pd
import matplotlib.pyplot as plt
import os

# === Load dataset ===
df = pd.read_csv('SBDB_sorted_DSH.csv', low_memory=False)

# === Create output folders ===
plot_dir = "orbital_plots"
scatter_dir = os.path.join(plot_dir, "scatter")
os.makedirs(plot_dir, exist_ok=True)
os.makedirs(scatter_dir, exist_ok=True)

# === Optional: cleaner labels for kind ===
kind_map = {
    'an': 'Asteroid (numbered)', 'au': 'Asteroid (unnumbered)',
    'cn': 'Comet (numbered)', 'cu': 'Comet (unnumbered)'
}
df['kind_label'] = df['kind'].map(kind_map).fillna(df['kind'])

# === Recalculate perihelion if missing ===
if 'q' not in df.columns or df['q'].isnull().all():
    df['q'] = df['a'] * (1 - df['e'])

# === D_SH Histogram ===
if 'D_SH to Next Row' in df.columns:
    plt.figure(figsize=(10, 6))
    plt.hist(df['D_SH to Next Row'].dropna(), bins=100)
    plt.title('Distribution of D_SH to Next Row')
    plt.xlabel('D_SH')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f"{plot_dir}/D_SH_distribution.png")
    plt.close()

# === Apply limits to remove extreme outliers ===
limits = {
    'e': (0, 1.2),
    'a': (0, 50),
    'i': (0, 180),
    'w': (0, 360),
    'om': (0, 360),
    'q': (0, 50)
}

# === Histogram plots (filtered) ===
hist_targets = {
    'e': 'Eccentricity',
    'a': 'Semimajor Axis (a)',
    'i': 'Inclination (°)',
    'w': 'Argument of Perihelion (°)',
    'om': 'Longitude of Ascending Node (°)',
    'q': 'Perihelion Distance (AU)'
}
for key, label in hist_targets.items():
    if key in df.columns: 
        data = df[key].dropna()
        low, high = limits.get(key, (data.min(), data.max()))
        data = data[(data >= low) & (data <= high)]
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=100)
        plt.title(f'Distribution of {label}')
        plt.xlabel(label)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(f"{plot_dir}/{key}_distribution.png")
        plt.close()
  


# === SCATTER PLOTS ===
scatter_pairs = [
    ('a', 'e'), ('a', 'i'), ('a', 'q'), ('om', 'a'), ('w', 'a'),
    ('i', 'e'), ('q', 'e'), ('om', 'e'), ('w', 'e'),
    ('q', 'i'), ('om', 'i'), ('w', 'i'),
    ('om', 'q'), ('w', 'q'),
    ('om', 'w')
]


def filter_outliers(df_part):
    return df_part[
        (df_part['e'].between(0, 1.2, inclusive='both')) &
        (df_part['a'].between(0.001, 50, inclusive='both')) &
        (df_part['q'].between(0.001, 50, inclusive='both')) &
        (df_part['i'].between(0, 180, inclusive='both')) &
        (df_part['om'].between(0, 360, inclusive='both')) &
        (df_part['w'].between(0, 360, inclusive='both'))
    ].dropna(subset=['a', 'e', 'i', 'q', 'w', 'om'])


def plot_scatter(filtered_df, label):
    for x, y in scatter_pairs:
        if x in filtered_df.columns and y in filtered_df.columns:
            sub_df = filtered_df[[x, y]].dropna()
            if sub_df.empty:
                print(f"⚠️ Skipped {label}_{y}_vs_{x}: no data after filtering.")
                continue
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(sub_df[x], sub_df[y], s=1, alpha=0.4, edgecolors='none')
            ax.set_title(f'{label}: {y} vs {x}')
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_xlim(limits.get(x, (None, None)))
            ax.set_ylim(limits.get(y, (None, None)))
            plt.tight_layout()
            filename = f"{scatter_dir}/{label}_{y}_vs_{x}.png"
            plt.savefig(filename)
            plt.close()
            print(f"✅ Saved: {filename}")
        else:
            print(f"❌ Missing columns for {label}_{y}_vs_{x}: {x} or {y}")



# ✅ Filter and plot by object kind
if 'kind' in df.columns:
    df['kind'] = df['kind'].astype(str)
    df_asteroids = filter_outliers(df[df['kind'].str.startswith('a')])
    df_comets = filter_outliers(df[df['kind'].str.startswith('c')])
    plot_scatter(df_asteroids, "Asteroids")
    plot_scatter(df_comets, "Comets")
else:
    df_filtered = filter_outliers(df)
    plot_scatter(df_filtered, "AllObjects")

print("✅ All cleaned plots saved in 'orbital_plots'")
