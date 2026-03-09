import pandas as pd
import telebot
import time
import requests
from binance.client import Client

# --- НАСТРОЙКИ (Заполни свои данные) ---
TOKEN = "ТВОЙ_ТЕЛЕГРАМ_ТОКЕН"
CHAT_ID = "ТВОЙ_CHAT_ID"
MODEL = "tinyllama:latest"

# Инициализация
bot = telebot.TeleBot(TOKEN)
client = Client() # Для публичных данных ключи не обязательны
last_price = None

def get_market_data():
    """Получаем данные с Binance и считаем индикаторы"""
    try:
        # Берем данные за последние 12 часов
        klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "12 hours ago UTC")
        df = pd.DataFrame(klines).iloc[:, [0, 4]]
        df.columns = ['time', 'close']
        df['close'] = pd.to_numeric(df['close'])
        
        # Расчет RSI
        delta = df['close'].diff()
        up = delta.clip(lower=0).rolling(window=14).mean()
        down = -delta.clip(upper=0).rolling(window=14).mean()
        rsi_val = 100 - (100 / (1 + (up / down.replace(0, 0.001))))
        
        # Расчет тренда (скользящая средняя за 20 периодов)
        sma = df['close'].rolling(window=20).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        trend = "ВВЕРХ 📈" if current_price > sma else "ВНИЗ 📉"
        
        return {
            "price": float(current_price),
            "rsi": round(rsi_val.iloc[-1], 2),
            "trend": trend
        }
    except Exception as e:
        print(f"❌ Ошибка Binance: {e}")
        return None

def ask_llama(data, change):
    """Запрос к локальной TinyLlama через Ollama"""
    url = "http://localhost:11434/api/generate"
    prompt = (f"Ты — аналитик OpenClaw. Рынок BTC изменился на {change:.2f}%. "
              f"Цена: {data['price']}, RSI: {data['rsi']}, Тренд: {data['trend']}. "
              f"Дай ОЧЕНЬ краткий совет трейдеру на русском языке.")
    
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json().get('response', 'Лама не смогла сформулировать ответ.')
    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama не запущена. Проверь приложение Ollama в трее!"
    except Exception as e:
        return f"⚠️ Ошибка нейросети: {str(e)}"

def send_alert(market_data, diff):
    """Формирование и отправка красивого сообщения"""
    advice = ask_llama(market_data, diff)
    
    msg = (
        f"🦞 *OpenClaw Sentinel 2026 Alert*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *Цена:* ${market_data['price']:,.2f} ({diff:+.2f}%)\n"
        f"📊 *RSI:* {market_data['rsi']}\n"
        f"📈 *Тренд:* {market_data['trend']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 *Совет Ламы:* {advice}"
    )
    
    try:
        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
        print("✅ Сообщение в Telegram отправлено!")
    except Exception as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")

print("📡 OpenClaw Sentinel 2026 запущен...")
print("Система мониторинга Binance + TinyLlama готова к работе.")

while True:
    market = get_market_data()
    
    if market:
        curr_p = market['price']
        if last_price:
            diff = ((curr_p - last_price) / last_price) * 100
            
            # Порог срабатывания (0.01% для теста)
            if abs(diff) >= 0.01:
                print(f"🔔 Зафиксировано движение: {diff:.2f}%")
                send_alert(market, diff)
        
        last_price = curr_p
    
    print("⏳ Ожидание 60 сек...")
    time.sleep(60)

  
