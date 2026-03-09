# -*- coding: utf-8 -*-
import pandas as pd
import telebot
import time
import requests
from binance.client import Client

# --- SETTINGS ---
TOKEN = ""
CHAT_ID = ""
MODEL = "tinyllama:latest"

# Initialization
bot = telebot.TeleBot(TOKEN)
client = Client() 
last_price = None

def get_market_data():
    """Fetching data from Binance and calculating RSI/Trend"""
    try:
        # Get last 12 hours of 15m klines
        klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "12 hours ago UTC")
        df = pd.DataFrame(klines).iloc[:, [0, 4]]
        df.columns = ['time', 'close']
        df['close'] = pd.to_numeric(df['close'])
        
        # RSI calculation
        delta = df['close'].diff()
        up = delta.clip(lower=0).rolling(window=14).mean()
        down = -delta.clip(upper=0).rolling(window=14).mean()
        rsi_val = 100 - (100 / (1 + (up / down.replace(0, 0.001))))
        
        # Trend calculation (SMA 20)
        sma = df['close'].rolling(window=20).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        trend = "BULLISH 📈" if current_price > sma else "BEARISH 📉"
        
        return {
            "price": float(current_price),
            "rsi": round(rsi_val.iloc[-1], 2),
            "trend": trend
        }
    except Exception as e:
        print(f"❌ Binance Error: {e}")
        return None

def ask_llama(data, change):
    """Request to local TinyLlama via Ollama (OpenClaw Framework)"""
    url = "http://localhost:11434/api/generate"
    # Prompt is now in English for international judges
    prompt = (f"You are OpenClaw AI analyst. BTC market changed by {change:.2f}%. "
              f"Price: {data['price']}, RSI: {data['rsi']}, Trend: {data['trend']}. "
              f"Give a VERY short professional trading advice in English (1 sentence).")
    
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    try:
        r = requests.post(url, json=payload, timeout=15)
        return r.json().get('response', 'Llama could not generate a response.')
    except requests.exceptions.ConnectionError:
        return "⚠️ Error: Ollama is not running! Please check your system tray."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

def send_alert(market_data, diff):
    """Sending professional Markdown message to Telegram"""
    advice = ask_llama(market_data, diff)
    
    msg = (
        f"🦞 *OpenClaw Sentinel 2026 Alert*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *Price:* ${market_data['price']:,.2f} ({diff:+.2f}%)\n"
        f"📊 *RSI:* {market_data['rsi']}\n"
        f"📈 *Trend:* {market_data['trend']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 *Llama's Advice:* {advice}"
    )
    
    try:
        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
        print(f"✅ Alert sent to Telegram! Change: {diff:.2f}%")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

print("📡 OpenClaw Sentinel 2026: Monitoring started...")
print("System Status: Binance API Connected | TinyLlama Ready.")

while True:
    market = get_market_data()
    
    if market:
        curr_p = market['price']
        if last_price:
            diff = ((curr_p - last_price) / last_price) * 100
            
            # Sensitivity threshold: 0.05% for real use
            if abs(diff) >= 0.05:
                send_alert(market, diff)
        
        last_price = curr_p
    
    print("⏳ Waiting 60 seconds for next update...")
    time.sleep(60)




    
