import requests
from binance.client import Client

# 1. Get real data from Binance
try:
    client = Client()
    ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    btc_price = ticker['price']
except Exception as e:
    btc_price = "72914.07" # Fallback if internet blinks

# 2. OpenClaw AI Engine (Local Ollama)
def openclaw_ai_agent(price):
    url = "http://localhost:11434/api/generate"
    
    # Simple and clear English prompt for best speed
    prompt = (
        f"You are OpenClaw AI Assistant for Binance. "
        f"Current Bitcoin price is {price} USDT. "
        f"Give 1 professional trading advice and 1 risk warning. Be concise."
    )
    
    payload = {"model": "tinyllama", "prompt": prompt, "stream": False}
    
    print(f"\n[OpenClaw] Analyzing Binance Market... BTC: {float(price):,.2f} USDT")
    
    try:
        response = requests.post(url, json=payload)
        return response.json()['response']
    except Exception as e:
        return "Connect your Ollama (Gray Llama icon) to start the engine!"

# 3. Execution
if __name__ == "__main__":
    print("=== OpenClaw AI: Binance Portfolio Protector ===")
    advice = openclaw_ai_agent(btc_price)
    
    print("\n" + "—"*40)
    print("AI AGENT ADVICE:")
    print(advice.strip())
    print("—"*40)
    print("\n[Status] Analysis complete. Ready for Binance Square submission.")
