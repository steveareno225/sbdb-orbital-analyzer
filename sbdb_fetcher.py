import requests
import pandas as pd
import time

# 💾 Output file
output_file = "sbdb_query_results.csv"

# 📋 All extracted fields from your CSV
fields = [
    'spkid','full_name','kind','pdes','name','prefix','neo','pha','sats',
    'H','G','M1','M2','K1','K2','PC','diameter','extent','albedo','rot_per','GM',
    'BV','UB','IR','spec_B','spec_T','H_sigma','diameter_sigma','orbit_id',
    'epoch','epoch_mjd','epoch_cal','equinox','e','a','q','i','om','w','ma','ad',
    'n','tp','tp_cal','per','per_y','moid','moid_ld','moid_jup','t_jup',
    'sigma_e','sigma_a','sigma_q','sigma_i','sigma_om','sigma_w','sigma_ma',
    'sigma_ad','sigma_n','sigma_tp','sigma_per','class','producer','data_arc',
    'first_obs','last_obs','n_obs_used','n_del_obs_used','n_dop_obs_used',
    'condition_code','rms','two_body','A1','A1_sigma','A2','A2_sigma',
    'A3','A3_sigma','DT','DT_sigma'
]


# 🛰️ API setup
api_url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
limit = 100000
offset = 0
all_data = []
total_fetched = 0

print("[🚀] Starting paginated fetch of all SBDB objects...")

while True:
    params = {
        "fields": ",".join(fields),
        "full-prec": "true",
        "limit": limit,
        "limit-from": offset
    }

    print(f"[📡] Fetching records {offset} to {offset + limit}...")
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        print(f"[❌] Request failed with status {response.status_code}")
        break

    data = response.json()
    rows = data.get("data", [])
    if not rows:
        print("[✅] No more data returned. Download complete.")
        break

    # Append to master list
    df_chunk = pd.DataFrame(rows, columns=data["fields"])
    all_data.append(df_chunk)

    total_fetched += len(df_chunk)
    print(f"[📦] Fetched: {total_fetched:,} objects so far...")

    # 🚀 Prepare for next round
    offset += limit
    time.sleep(1)  # 🔄 Optional: Be kind to the API

# 🧾 Final save
print("[💾] Concatenating all data and writing to CSV...")
final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv(output_file, index=False)
print(f"[🎯] Saved {total_fetched:,} records to {output_file}")
