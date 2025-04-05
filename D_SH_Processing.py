import pandas as pd
import math

# Load sbdb_query_results CSV file
file_path = 'sbdb_query_results.csv'

# Load all columns as strings to avoid DtypeWarnings
df = pd.read_csv(file_path, dtype=str)

# Convert orbital element columns to numeric
cols_to_convert = ['a', 'e', 'i', 'w', 'om', 'q']
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with NaNs in required calculation fields
df = df.dropna(subset=['a', 'e'])

# Add rounded columns for sorting
df['ecc_round'] = df['e'].round(2)
df['a_round'] = df['a'].round(1)
df['i_round'] = df['i'].round(-1)
df['peri_round'] = df['w'].round(-1)
df['node_round'] = df['om'].round(-1)

# Sort dataset by rounded orbital elements
df_sorted = df.sort_values(by=['node_round', 'i_round', 'peri_round', 'a_round', 'ecc_round']).reset_index(drop=True)
# If perihelion distance is missing, calculate it
if df_sorted['q'].isnull().all():
    df_sorted['q'] = df_sorted['a'] * (1 - df_sorted['e'])

# D_SH function
def calculate_d_sh(row1, row2):
    try:
        e1, q1, i1, node1, peri1 = row1['e'], row1['q'], row1['i'], row1['om'], row1['w']
        e2, q2, i2, node2, peri2 = row2['e'], row2['q'], row2['i'], row2['om'], row2['w']
        i1, i2 = math.radians(i1), math.radians(i2)
        node1, node2 = math.radians(node1), math.radians(node2)
        peri1, peri2 = math.radians(peri1), math.radians(peri2)
        Pi1, Pi2 = node1 + peri1, node2 + peri2
        term1 = (e1 - e2)**2
        term2 = (q1 - q2)**2
        cosI = math.cos(i1)*math.cos(i2) + math.sin(i1)*math.sin(i2)*math.cos(node1 - node2)
        I = math.acos(min(max(cosI, -1.0), 1.0))
        term3 = (2 * math.sin(I / 2))**2
        term4 = ((e1 + e2)/2)**2 * (2 * math.sin((Pi1 - Pi2)/2))**2
        return math.sqrt(term1 + term2 + term3 + term4)
    except:
        return None

# Calculate D_SH for consecutive rows
dsh_scores = [calculate_d_sh(df_sorted.iloc[i], df_sorted.iloc[i+1]) for i in range(len(df_sorted)-1)]
dsh_scores.append(None)
df_sorted['D_SH to Next Row'] = dsh_scores

# Save the full sorted file with D_SH
df_sorted.to_csv('SBDB_sorted_DSH.csv', index=False)

# Extract rows below thresholds
def get_pairs_below_threshold(df, threshold):
    indices = []
    for i in range(len(df) - 1):
        if df.at[i, 'D_SH to Next Row'] is not None and df.at[i, 'D_SH to Next Row'] < threshold:
            indices.extend([i, i+1])
    return df.loc[sorted(set(indices))]

# Export multiple threshold files
get_pairs_below_threshold(df_sorted, 0.01).to_csv('D_SH_filtered_below_001.csv', index=False)
get_pairs_below_threshold(df_sorted, 0.05).to_csv('D_SH_filtered_below_005.csv', index=False)
get_pairs_below_threshold(df_sorted, 0.10).to_csv('D_SH_filtered_below_010.csv', index=False)
get_pairs_below_threshold(df_sorted, 0.50).to_csv('D_SH_filtered_below_050.csv', index=False)
get_pairs_below_threshold(df_sorted, 1.00).to_csv('D_SH_filtered_below_100.csv', index=False)

print("✅ Script complete. Filtered D_SH datasets exported.")
