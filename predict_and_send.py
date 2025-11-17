import os
import json
import time
import joblib
import requests
import pandas as pd
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from keras.losses import MeanSquaredError
from web3 import Web3

# ======================================================
# 1️⃣ ENVIRONMENT
# ======================================================
load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT = Web3.to_checksum_address(os.getenv("ACCOUNT_ADDRESS"))
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

if not all([INFURA_URL, PRIVATE_KEY, ACCOUNT, ETHERSCAN_API_KEY]):
    raise Exception(" Missing environment variables in .env")

# ======================================================
# 2️⃣ CONNECT TO SEPOLIA
# ======================================================
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise Exception(" Connection failed to Sepolia.")
print(" Connected to Sepolia via Infura\n")

# ======================================================
# 3️⃣ SMART CONTRACT
# ======================================================
with open("blockchain/GasOptimizer_abi.json", "r") as f:
    abi = json.load(f)
with open("blockchain/GasOptimizer_address.txt", "r") as f:
    contract_address = f.read().strip()

contract = w3.eth.contract(address=contract_address, abi=abi)
print(f" Connected to Smart Contract at: {contract_address}\n")

# ======================================================
# 4️⃣ MODEL & SCALER
# ======================================================
print(" Loading trained LSTM model and scaler...")
model = load_model("gas_lstm_model.h5", compile=False)
model.compile(optimizer='adam', loss=MeanSquaredError())
scaler = joblib.load("lstm_scaler.joblib")
print(" Model and scaler loaded successfully.\n")

# ======================================================
# 5️⃣ CSV SETUP
# ======================================================
GAS_CSV = "new_blockchain.csv"

if not os.path.exists(GAS_CSV):
    raise Exception(f" CSV file {GAS_CSV} not found — please ensure your dataset exists.")

# ======================================================
# 6️⃣ APPEND LIVE GAS DATA TO EXISTING CSV
# ======================================================
def update_gas_csv():
    """Fetch live gas price and append to existing blockchain CSV properly."""
    url = "https://api.blocknative.com/gasprices/blockprices"
    headers = {"Authorization": "BN.api-demo-key"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        gas_gwei = float(data["blockPrices"][0]["estimatedPrices"][0]["price"])
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        df = pd.read_csv(GAS_CSV)

        # Prepare a blank new row (same columns)
        new_row = {col: None for col in df.columns}

        # Fill only the known fields
        if "Timestamp" in new_row:
            new_row["Timestamp"] = timestamp
        if "Gas_Price_Gwei" in new_row:
            new_row["Gas_Price_Gwei"] = gas_gwei

        # Append & save
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(GAS_CSV, index=False)

        print(f" Live gas price fetched: {gas_gwei} Gwei → Appended to dataset")
        return gas_gwei

    except Exception as e:
        print(" Failed to fetch live gas data:", e)
        raise

def show_gas_csv():
    df = pd.read_csv(GAS_CSV).dropna(subset=["Gas_Price_Gwei"])
    print("\nLast 20 rows of CSV used for prediction:")
    print(df.tail(20).to_string(index=False))
    print("\n")

# ======================================================
# 7️⃣ LSTM PREDICTION
# ======================================================
def predict_gas_price():
    df = pd.read_csv(GAS_CSV)
    df = df.dropna(subset=["Gas_Price_Gwei"])
    df = df.tail(100)
    series = df["Gas_Price_Gwei"].astype(float).values.reshape(-1, 1)
    scaled = scaler.transform(series)

    SEQ_LEN = 24
    if len(scaled) < SEQ_LEN:
        raise Exception("Not enough data for prediction.")

    x_input = scaled[-SEQ_LEN:].reshape(1, SEQ_LEN, 1)
    pred_scaled = model.predict(x_input, verbose=0)
    predicted_gas = scaler.inverse_transform(pred_scaled)[0][0]
    return round(float(predicted_gas), 2)

# ======================================================
# 8️⃣ OPTIMIZE + EXECUTE
# ======================================================
def optimize_and_execute():
    threshold = contract.functions.threshold().call()
    print(f" Smart Contract Threshold: {threshold} Gwei")

    # ✅ Get latest live gas price
    gas_gwei = update_gas_csv()

    # ✅ Predict gas price using LSTM
    predicted = predict_gas_price()

    # ✅ Adjust the predicted price closer to live feed
    predicted = (gas_gwei + 0.1 * (predicted - gas_gwei)) - 0.02
    predicted = predicted * 10

    show_gas_csv()
    print(f"🔹 Predicted Gas Price: {predicted} Gwei")

    # ✅ Keep optimizing until it goes below threshold
    while predicted > threshold:
        print(f" Predicted {predicted} > threshold {threshold} → recalculating...")
        gas_gwei = update_gas_csv()
        show_gas_csv()
        time.sleep(10)
        predicted = predict_gas_price()
        predicted = (gas_gwei + 0.1 * (predicted - gas_gwei)) - 0.02
        predicted = predicted * 10

    print(f" Optimized Gas Price: {predicted} Gwei (≤ threshold)\n")

    # ✅ Build & send transaction
    nonce = w3.eth.get_transaction_count(ACCOUNT)
    txn = contract.functions.executeTransaction().build_transaction({
        'from': ACCOUNT,
        'chainId': 11155111,
        'gas': 200000,
        'gasPrice': w3.to_wei(predicted, 'gwei'),
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    raw_tx = getattr(signed_txn, "rawTransaction", None) or getattr(signed_txn, "raw_transaction", None)
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    print(f" Transaction sent successfully! Tx Hash: {tx_hash.hex()}\n")

# ======================================================
# 9️⃣ MAIN
# ======================================================
if __name__ == "__main__":
    print(" Starting Gas Price Optimization...\n")
    try:
        update_gas_csv()  # Appends live gas price to your blockchain dataset
        optimize_and_execute()
        print(" Smart contract executed successfully with optimized gas price.\n")
    except Exception as e:
        print(" Error:", e)
