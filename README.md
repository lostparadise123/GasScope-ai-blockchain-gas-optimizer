# 🚀 GasScope — AI + Blockchain Gas Optimizer  
### AI-powered gas fee prediction + automated Sepolia smart contract execution

## 📌 Overview
*GasScope* predicts Ethereum gas fees and automatically executes a smart contract only when gas prices are low.  
It combines:

- 🧠 *LSTM deep learning* for gas forecasting  
- ⚡ *Real-time gas feed* via Blocknative API  
- 🔗 *Web3.py* blockchain interaction  
- 🤖 *Auto smart-contract execution* based on thresholds  
- 📊 *Streamlit dashboard* for live monitoring  

This system helps avoid high gas fees by executing transactions at the most cost-efficient time.

---

## 🔥 Features

### ✅ AI-Based Gas Forecasting
- LSTM model trained on historical gas data  
- Predicts next-step gas using 24-time-step sequences  
- Live-adjusted prediction for higher accuracy  

### ✅ Real-Time Gas Tracking
- Fetches live gas feed (Blocknative API)  
- Continuously updates new_blockchain.csv  

### ✅ Blockchain Automation (Sepolia)
Auto-calls your smart contract when: optimized_prediction <= smart_contract_threshold

- Uses Web3.py + Infura  
- Ensures execution only during *low gas windows*

### ✅ Streamlit UI
- Live gas feed graph  
- Real-time LSTM predictions  
- Smart contract threshold viewer  
- One-click *Optimize + Execute*  
- Shows last 20 gas entries  

---

## 📸 Screenshots

<img width="1886" height="909" alt="Screenshot" src="https://github.com/user-attachments/assets/dd5df129-33c1-41d8-874a-7fe4cef87985" />

<img width="1909" height="971" alt="Screenshot" src="https://github.com/user-attachments/assets/51fa78ea-7a07-441f-9d5a-ee215c5e16fc" />

<img width="1895" height="917" alt="Screenshot" src="https://github.com/user-attachments/assets/688d11c0-928e-4004-88c0-48c4e15520ac" />

---
