# 🦞 ClawGuard AI: Local Telegram Sentinel for Binance
**Built for the #AIBinance Challenge using the OpenClaw Framework.**

## 🚀 Overview
ClawGuard AI is a high-performance, privacy-focused AI assistant that monitors the **Binance** market and sends real-time trading advice directly to your **Telegram**. 

Unlike standard bots, it runs a **local LLM (TinyLlama)** on your machine via **Ollama**, ensuring your data and strategy stay 100% private.

## ✨ Key Features
- **Real-Time Data:** Fetches live BTC/USDT prices directly from Binance API.
- **Local AI Brain:** Uses `tinyllama` to generate professional trading insights without internet-based AI fees.
- **Telegram Integration:** Sends instant market reports and risk warnings to your phone.
- **Hardware Optimized:** Engineered to run smoothly even on 5-year-old laptops.
- **Privacy First:** Your API keys and trading thoughts never leave your local hardware.

## 🛠️ Tech Stack
- **Framework:** [OpenClaw](https://github.com)
- **Engine:** [Ollama](https://ollama.com)
- **Language:** Python 3.10+
- **APIs:** Binance Public API & Telegram Bot API

## 📦 Installation & Setup
1. **Install Ollama:** Download and run `ollama run tinyllama`.
2. **Install Dependencies:**
   ```bash
   pip install python-binance pyTelegramBotAPI requests

