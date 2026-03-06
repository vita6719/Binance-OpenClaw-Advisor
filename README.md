🦞 OpenClaw: Local AI Market Sentinel
OpenClaw — это легковесный аналитический фреймворк на базе Python, который объединяет мощь Binance API и локальных языковых моделей (Ollama) для создания автономного торгового ассистента.
Проект создан в рамках конкурса #AIBinance.
✨ Основные возможности
🚀 Real-time Monitoring: Прямое подключение к Binance API для отслеживания пары BTC/USDT.
🧠 Local Intelligence: Использование модели TinyLlama (через Ollama) для анализа рынка без облачных запросов и платных подписок.
📊 Technical Analysis: Автоматический расчет индикатора RSI и определение тренда.
🔔 Smart Alerts: Система отправляет уведомления в Telegram только при значимых изменениях цены (защита от рыночного шума).
🛡️ Privacy First: Все вычисления происходят локально на вашем устройстве.
🛠 Стек технологий
Language: Python 3.10+
AI Engine: Ollama (Model: TinyLlama / Gemma)
Framework: OpenClaw Logic
Libraries: pandas, python-binance, pyTelegramBotAPI, requests
🚀 Быстрый старт
Установите Ollama и скачайте модель:
bash
ollama run tinyllama
Используйте код с осторожностью.

Установите зависимости:
bash
pip install pandas python-binance pyTelegramBotAPI requests
Используйте код с осторожностью.

Настройте Telegram:
Создайте бота через @BotFather и вставьте свой TOKEN и CHAT_ID в код.
Запустите стража:
bash
python binance_ai.py
Используйте код с осторожностью.

📝 Дисклеймер
Данный проект создан в образовательных целях и не является финансовой рекомендацией. Торговля криптовалютой сопряжена с высокими рисками.
⭐ Разработано для сообщества Binance Square.
