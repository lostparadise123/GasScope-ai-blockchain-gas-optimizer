import streamlit as st
import pandas as pd
from predict_and_send import (
    update_gas_csv,
    predict_gas_price,
    optimize_and_execute,
    contract,
)

st.set_page_config(page_title="GasScope Optimizer", layout="centered")

st.title("⛽ GasScope — AI + Blockchain Gas Optimizer")
st.write("Live Gas Tracking • LSTM Prediction • Sepolia Smart Contract Execution")

# ----------------------------------------------------------
# Smart Contract Threshold
# ----------------------------------------------------------
with st.container():
    st.subheader("📌 Smart Contract Threshold")
    try:
        threshold = contract.functions.threshold().call()
        st.success(f"Current Contract Threshold: **{threshold} Gwei**")
    except Exception as e:
        st.error(f"Error fetching threshold: {e}")

# ----------------------------------------------------------
# Fetch Live Gas
# ----------------------------------------------------------
st.subheader("📡 Fetch Live Gas Price")

if st.button("Fetch Gas Price", key="fetch"):
    try:
        gas = update_gas_csv()
        st.success(f"Live Gas Price Added: **{gas} Gwei**")
    except Exception as e:
        st.error(f"Error: {e}")

# ----------------------------------------------------------
# EXACT TERMINAL-LIKE PREDICTION (WITHOUT EXECUTION)
# ----------------------------------------------------------
st.subheader("🤖 Predict Gas Price — Synced with Terminal")

if st.button("Predict Gas Price", key="predict"):
    try:
        # 1️⃣ live gas
        live_gas = update_gas_csv()

        # 2️⃣ raw lstm
        raw_pred = predict_gas_price()

        # 3️⃣ SAME formula as optimize_and_execute()
        optimized = (live_gas + 0.1 * (raw_pred - live_gas)) - 0.02
        optimized = optimized * 10
        optimized = round(optimized, 3)

        st.info(
            f"""
### 🔍 Terminal Synced Prediction  
**Live Gas:** {live_gas} Gwei  
**LSTM Raw Prediction:** {raw_pred} Gwei  

### ✅ FINAL Optimized Prediction: **{optimized} Gwei**
            """
        )

    except Exception as e:
        st.error(f"Error: {e}")

# ----------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------
st.subheader("⚙️ Optimize & Execute Smart Contract")

if st.button("Run Full Optimization & Execute", key="execute_btn"):
    try:
        with st.spinner("Running optimization and sending transaction..."):
           tx_hash = optimize_and_execute()  # backend handles everything

           st.success(f"🎉 Transaction executed!\n\n**Tx Hash:** `{tx_hash}`")

    except Exception as e:
        st.error(f"Execution error: {e}")

# ----------------------------------------------------------
# Show last 20 CSV rows
# ----------------------------------------------------------
st.subheader("📄 Last 20 Gas Records")

try:
    df = pd.read_csv("new_blockchain.csv").dropna(subset=["Gas_Price_Gwei"])
    st.dataframe(df.tail(20))
except Exception as e:
    st.error(f"CSV error: {e}")
