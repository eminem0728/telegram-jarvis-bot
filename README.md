# 🤖 Telegram Jarvis Bot

Умный Telegram-ассистент, который отвечает на вопросы и ищет изображения.

## Возможности

- **Ответы на вопросы**: `Джарвис, что такое квантовый компьютер?`
- **Поиск фото**: `Джарвис, покажи Эйфелеву башню`
- **Работа в группах**: реагирует на `@botusername`
- **24/7**: работает на хостинге без твоего ПК

## Быстрый старт (локально)

```bash
# 1. Клонируй
cd telegram-jarvis-bot

# 2. Установи зависимости
pip install -r requirements.txt

# 3. Настрой .env
cp .env.example .env
# Открой .env и вставь token от @BotFather

# 4. Запусти
python main.py
```

## Хостинг 24/7 (бесплатно)

### Вариант 1: Render.com (рекомендую)

1. Залей код на GitHub: `C:\Users\gurba\telegram-jarvis-bot`
2. Зарегистрируйся на https://render.com (через GitHub)
3. Нажми **New +** → **Web Service**
4. Подключи свой репозиторий
5. Настрой:
   - **Name**: `telegram-jarvis-bot`
   - **Runtime**: `Docker`
   - **Branch**: `main`
   - **Plan**: Free
6. В разделе **Environment** добавь переменные (из .env):
   - `TELEGRAM_TOKEN`
   - `AI_PROVIDER` = `openai`
   - `OPENAI_API_KEY`
7. Нажми **Deploy**

Через 5 минут бот будет работать 24/7.

### Вариант 2: Railway.app

1. Залей код на GitHub
2. Зайди на https://railway.app
3. **New Project** → **Deploy from GitHub repo**
4. Добавь переменные окружения (те же, что в .env)
5. Жди деплоя

### Вариант 3: Oracle Cloud (навсегда бесплатно)

Можно поднять VM на Always Free Tier и запустить бота через tmux или systemd.

## Переменные окружения

| Переменная | Описание | Обязательно |
|---|---|---|
| `TELEGRAM_TOKEN` | Токен от @BotFather | ✅ Да |
| `AI_PROVIDER` | `openai` / `gemini` / `web` | ❌ (по умолч. `openai`) |
| `OPENAI_API_KEY` | API ключ OpenAI | ❌ (если AI_PROVIDER=openai) |
| `OPENAI_MODEL` | Модель GPT (напр. `gpt-4o-mini`) | ❌ |
| `GEMINI_API_KEY` | API ключ Google Gemini | ❌ (если AI_PROVIDER=gemini) |

## AI провайдеры

### OpenAI (ChatGPT)
Нужен API ключ. Получить: https://platform.openai.com/api-keys

### Google Gemini (бесплатно)
Нужен API ключ. Получить: https://makersuite.google.com/app/apikey

### Web (без API ключа)
Использует DuckDuckGo поиск. Не требует ключей, но отвечает только ссылками.
