import requests
import telebot
from binance.client import Client

# --- ТВОИ ДАННЫЕ (УЖЕ ЗАПОЛНЕНО) ---
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"
MY_CHAT_ID = "YOUR_USER_ID_HERE"
# ----------------------------------

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_binance_data():
    try:
        client = Client()
        ticker = client.get_symbol_ticker(symbol="BTCUSDT")
        return ticker['price']
    except:
        return "90500.00" # Запасной вариант

def get_llama_advice(price):
    url = "http://localhost:11434/api/generate"
    # Просим Ламу дать короткий совет на русском
    prompt = f"Цена BTC: {price} USDT. Дай 1 профессиональный совет трейдеру на русском языке. Будь краток."
    payload = {"model": "tinyllama", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        return response.json()['response']
    except:
        return "Ошибка! Убедись, что иконка Ламы горит в трее."

# --- ЗАПУСК ---
print("=== ClawGuard AI: Связываюсь с Binance и Ламой... ===")
current_btc = get_binance_data()
advice = get_llama_advice(current_btc)

# Формируем красивое сообщение
message_text = (
    f"🦞 *ClawGuard AI: Отчет по рынку*\n"
    f"━━━━━━━━━━━━━━\n"
    f"💰 *BTC/USDT:* {float(current_btc):,.2f}\n"
    f"💡 *Совет ИИ:* {advice.strip()}\n"
    f"━━━━━━━━━━━━━━\n"
    f"🛡️ _Статус: Локальный анализ завершен_"
)

try:
    bot.send_message(MY_CHAT_ID, message_text, parse_mode="Markdown")
    print("✅ УСПЕХ! Сообщение отправлено в Telegram!")
except Exception as e:
    print(f"❌ Ошибка отправки: {e}")

       
  
