# 🦞 ClawGuard AI: Your Local Binance Sentinel
Built with **OpenClaw** & **Ollama** for the #AIBinance Challenge.

## 🚀 Overview
ClawGuard AI is a privacy-first, local AI assistant designed to protect Binance users from emotional trading. Unlike cloud-based bots, it runs entirely on your machine using the **OpenClaw framework** and **Ollama**.

## ✨ Key Features
- **Local Intelligence:** Powered by `tinyllama` via Ollama. No data leaves your computer.
- **Live Market Sync:** Connects to **Binance API** to fetch real-time prices (BTC/USDT, etc.).
- **Risk Management:** Provides professional trading advice and volatility warnings based on live data.
- **Hardware Efficient:** Optimized to run even on 5-year-old laptops.

## 🛠️ Technical Stack
- **Framework:** [OpenClaw](https://github.com)
- **Engine:** [Ollama](https://ollama.com) (Model: `tinyllama`)
- **Language:** Python 3.10+
- **Library:** `python-binance`

## 📦 How to Run
1. Install Ollama and run `ollama run tinyllama`.
2. Install dependencies: `pip install openclaw python-binance requests`.
3. Run the script: `python binance_ai.py`.

## 🛡️ Privacy & Safety
This agent does **not** require "Withdrawal" permissions on your Binance API. It uses read-only access to provide sentiment and technical analysis locally.
