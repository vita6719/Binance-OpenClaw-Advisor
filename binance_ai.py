import pandas as pd
import telebot
import time
import requests # Прямой запрос к Ламе надежнее для 3.14
from binance.client import Client

# --- НАСТРОЙКИ ---
TOKEN = ""
CHAT_ID = ""
MODEL = "tinyllama:latest" # Или твоя tinyllama

bot = telebot.TeleBot(TOKEN)
client = Client()
last_price = None

def get_market_data():
    """Получаем данные и считаем RSI (упрощенно)"""
    try:
        # Берем последние 50 свечей
        klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "12 hours ago UTC")
        # Создаем таблицу только из нужных данных
        df = pd.DataFrame(klines).iloc[:, [0, 4]] # Оставляем Время и Close
        df.columns = ['time', 'close']
        df['close'] = pd.to_numeric(df['close'])
        
        # Считаем RSI (упрощенная формула для стабильности)
        delta = df['close'].diff()
        up = delta.clip(lower=0).rolling(window=14).mean()
        down = -delta.clip(upper=0).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (up / down.replace(0, 0.001))))
        
        return {
            "price": float(df['close'].iloc[-1]),
            "rsi": round(rsi.iloc[-1], 2),
            "trend": "ВВЕРХ" if df['close'].iloc[-1] > df['close'].rolling(window=20).mean().iloc[-1] else "ВНИЗ"
        }
    except Exception as e:
        print(f"❌ Ошибка данных: {e}")
        return None

def ask_llama(data, change):
    """Прямой запрос к Ollama (без LangChain, чтобы не было ошибок совместимости)"""
    url = "http://localhost:11434/api/generate"
    prompt = f"Рынок BTC изменился на {change:.2f}%. Цена: {data['price']}, RSI: {data['rsi']}, Тренд: {data['trend']}. Дай краткий совет трейдеру на русском."
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    try:
        r = requests.post(url, json=payload, timeout=60)
        return r.json()['response']
    except:
        return "Лама не отвечает, проверь трей!"

print("📡 OpenClaw Sentinel 2026: Старт мониторинга...")

while True:
    market = get_market_data()
    if market:
        curr_p = market['price']
        if last_price:
            diff = ((curr_p - last_price) / last_price) * 100
            # ДЛЯ ТЕСТА: срабатывает на ЛЮБОЕ изменение > 0.01%
            if abs(diff) > 0.01: 
                print(f"📈 Движение: {diff:.2f}%")
                advice = ask_llama(market, diff)
                msg = f"🦞 *OpenClaw Alert*\n💰 Цена: ${curr_p:,.2f} ({diff:+.2f}%)\n📊 RSI: {market['rsi']}\n🤖 Совет: {advice}"
                bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
        
        last_price = curr_p
    
    print("⏳ Ожидание 1 минуту...")
    time.sleep(60)

  
  
 
