import pandas as pd

# === Load the sorted D_SH dataset ===
df = pd.read_csv('SBDB_sorted_DSH.csv')

# === Define D_SH clustering threshold ===
threshold = 0.01
cluster_ids = []
current_cluster = 0

# === Assign cluster_id based on continuity of D_SH values ===
for i in range(len(df)):
    if i == 0 or df.loc[i - 1, 'D_SH to Next Row'] >= threshold:
        current_cluster += 1
    cluster_ids.append(current_cluster)

df['cluster_id'] = cluster_ids

# === Filter to include only clusters with 2 or more members ===
cluster_counts = df['cluster_id'].value_counts()
valid_clusters = cluster_counts[cluster_counts >= 2].index
df = df[df['cluster_id'].isin(valid_clusters)]

# === Create cleaned export with relevant columns ===
columns_to_export = [
    'full_name', 'a', 'e', 'i', 'w', 'om', 'q','ma',
    'ecc_round', 'a_round', 'i_round', 'peri_round', 'node_round',
    'D_SH to Next Row', 'cluster_id'
]
cleaned_df = df[columns_to_export].sort_values(by='cluster_id')

# === Save to CSV ===
output_file = 'Filtered_Clusters_2plus.csv'
cleaned_df.to_csv(output_file, index=False)

print(f"✅ Filtered cluster report exported to {output_file}")
