import pandas as pd
import time
from data_fetch import fetch_wallet_data
from score_model import calculate_score

# Load wallets
wallet_df = pd.read_csv("wallets.csv")
wallets = wallet_df["wallet_id"].tolist()

wallet_data = []
print("Fetching data for wallets...")

for wallet in wallets:
    print(f"Fetching wallet: {wallet}")  # ✅ Add this to see progress
    data = fetch_wallet_data(wallet)
    wallet_data.append(data)
    time.sleep(0.3)  # Prevent rate limiting

features_df = pd.DataFrame(wallet_data)
scored_df = calculate_score(features_df)
scored_df.to_csv("wallet_scores.csv", index=False)

print("✅ Risk scores saved to wallet_scores.csv")
