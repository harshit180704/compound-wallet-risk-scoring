import requests
import time

API_KEY = "cqt_rQFYmM9fbfBQPkvwx4JbVvHMHdyv"
CHAIN_ID = 1  # Ethereum mainnet

def fetch_wallet_data(wallet):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet}/transactions_v2/"
    params = {
        "key": API_KEY,
        "page-size": 1000
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # ✅ Safe access to nested fields
        if not data or not isinstance(data, dict):
            raise Exception("No response from Covalent")

        data_obj = data.get("data")
        if not data_obj or "items" not in data_obj:
            raise Exception("Missing 'items' in response")

        items = data_obj["items"]
        if not isinstance(items, list):
            raise Exception("'items' is not a list")

        total_borrowed = 0
        total_repaid = 0
        liquidation_count = 0
        interaction_count = 0

        for txn in items:
            interaction_count += 1

            logs = txn.get("log_events", [])
            if not isinstance(logs, list):
                continue

            for log in logs:
                if not isinstance(log, dict):
                    continue  # skip malformed logs

                sender = (log.get("sender_name") or "").lower()
                decoded = log.get("decoded")
                if not isinstance(decoded, dict):
                    continue  # skip if decoded is None

                name = decoded.get("name", "").lower()
                params = decoded.get("params", [])
                if not isinstance(params, list):
                    continue

                if "compound" in sender:
                    for p in params:
                        value = p.get("value")
                        if value is None:
                            continue
                        try:
                            amount = float(value)
                        except:
                            amount = 0

                        pname = p.get("name", "").lower()
                        if "borrow" in name and "amount" in pname:
                            total_borrowed += amount
                        elif "repay" in name and "amount" in pname:
                            total_repaid += amount
                        elif "liquidat" in name:
                            liquidation_count += 1

        return {
            "wallet_id": wallet,
            "total_borrowed": total_borrowed,
            "total_repaid": total_repaid,
            "liquidation_count": liquidation_count,
            "interaction_count": interaction_count
        }

    except Exception as e:
        print(f"Failed to fetch for {wallet}: {e}")
        return {
            "wallet_id": wallet,
            "total_borrowed": 0,
            "total_repaid": 0,
            "liquidation_count": 0,
            "interaction_count": 0
        }
