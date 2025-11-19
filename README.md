GasScope — AI + Blockchain Gas Optimizer
An AI-powered gas fee prediction & smart contract automation system using LSTM + Sepolia Blockchain
📌 Overview
GasScope is an AI-driven system designed to predict, optimize, and automatically execute Ethereum smart contracts only when gas prices are low.
It integrates:

LSTM deep learning for gas price forecasting

Real-time live gas feed (via Blocknative API)

Automated threshold-based execution of a Solidity smart contract

Blockchain interaction using Web3.py

Streamlit UI dashboard for live monitoring

This project solves the real-world challenge of high blockchain gas fees by enabling intelligent, automated contract execution at the most cost-efficient time.

🚀 Features
✅ AI-Based Gas Price Forecasting

Uses an LSTM model trained on historical gas prices

Predicts future gas cost using 24-time-step sequences

Adjusts prediction closer to live feed for accuracy

✅ Real-Time Gas Tracking

Fetches live gas data via Blocknative

Continuously appends to dataset (new_blockchain.csv)

✅ Blockchain Automation

Connects to Sepolia Testnet using Infura

Automatically triggers executeTransaction() when:

optimized_predicted_price ≤ smart_contract_threshold


Ensures transactions occur only during low gas price periods

✅ Streamlit UI

Live gas feed

Real-time predictions

Smart contract threshold viewer

One-click optimization + execution

Display of latest 20 gas records
<img width="1886" height="909" alt="Screenshot 2025-11-20 013909" src="https://github.com/user-attachments/assets/dd5df129-33c1-41d8-874a-7fe4cef87985" />
<img width="1909" height="971" alt="image" src="https://github.com/user-attachments/assets/51fa78ea-7a07-441f-9d5a-ee215c5e16fc" />

