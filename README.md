# 🧠 Compound Wallet Risk Scoring

This project scores Ethereum wallet addresses based on their historical interaction with the Compound V2 protocol using Covalent's API.

---

## 📊 Objective

Assign a **risk score (0–1000)** to 100 wallets based on:
- Borrow and repayment history
- Liquidations
- Number of protocol interactions

---

## 🛠️ Data Collection

- Source: [Covalent API](https://www.covalenthq.com/)
- Network: Ethereum Mainnet
- Endpoint used:  
  `https://api.covalenthq.com/v1/1/address/{wallet_address}/transactions_v2/`

Each wallet’s transactions are fetched, parsed, and filtered to include only those related to the Compound protocol.

---

## 📐 Feature Selection

| Feature             | Description                                           |
|---------------------|-------------------------------------------------------|
| `total_borrowed`    | Total volume borrowed from Compound                  |
| `total_repaid`      | Total repayments made                                |
| `liquidation_count` | Number of times wallet faced liquidation             |
| `interaction_count` | Number of times wallet interacted with Compound      |

These features are chosen based on their impact on **user creditworthiness** and **protocol health**.

---

## 🧮 Scoring Methodology

The scoring function is based on normalized features:

```python
repay_ratio = total_repaid / (total_borrowed or 1)

score = (
    0.3 * (1 - normalize(repay_ratio)) +
    0.3 * normalize(liquidation_count) +
    0.2 * normalize(total_borrowed) +
    0.2 * (1 - normalize(interaction_count))
) * 1000
Higher score → Higher risk

Scores are rounded to integers from 0 to 1000.

📁 Output
Results are stored in:

Copy
wallet_scores.csv
Example:

wallet_id	score
0x0039f22efb07a647557c7c5d17854cfd6d489ef3	692
0x06b51c6882b27cb05e712185531c1f74996dd988	510

🧰 Project Structure
compound_wallet_scoring/
├── main.py             # Main script to run the scoring
├── data_fetch.py       # Fetches and parses wallet transactions
├── score_model.py      # Defines the scoring logic
├── wallets.csv         # Input list of wallet addresses
├── wallet_scores.csv   # Output file with risk scores
└── __pycache__/        # Python cache (auto-generated)
🚀 How to Run
pip install -r requirements.txt  # Install required packages
python main.py                   # Run the scoring
Make sure wallets.csv is populated with wallet addresses before running.

🔑 API Key Setup
Open data_fetch.py and replace:

python
Copy
Edit
API_KEY = "your_covalent_api_key"
with your free Covalent API key.

📈 Scalability
Add more wallets easily via wallets.csv

Plug into any EVM-compatible chain by changing CHAIN_ID

Extend to support other DeFi protocols like Aave or MakerDAO

💡 Future Enhancements
Compound V3 support

Smart contract-based deployment

Web dashboard with interactive filtering

More advanced ML-based scoring

