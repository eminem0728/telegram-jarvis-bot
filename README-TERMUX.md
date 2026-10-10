# Джарвис на Termux (Realme Narzo 50)

Бот полностью переведён на телефон. Fly.io / Render больше не нужны.

## Что изменилось в коде

- `main.py` сам определяет Termux (`PHONE_MODE=1` или `/data/data/com.termux`):
  - health-сервер на порту 10000 **отключён** (был нужен только для Fly/Render)
  - все json (`extra_users`, `group_users`, `bot_groups`, `monitored_chats`) лежат в `./data/` и не теряются при рестарте
  - удалён GitHub-костыль с пушем `extra_users.json` (там был баг с `.hex()` вместо base64)
  - история: сутки / 1000 сообщений для всех чатов (было час / 200)
  - таймаут AI по умолчанию 120с (было 75)
  - `run_polling` в бесконечном цикле с backoff — сам поднимается после обрыва Wi-Fi
  - логи в `./logs/bot.log` с ротацией + уведомления `termux-notification`
  - голосовые теперь реально работают: расшифровка → ответ AI (раньше `handle_voice` просто делал `return`)
  - удалён дублированный сломанный `_tag_job_callback` (тегалка снова работает)
  - скачивание музыки/видео ставится на паузу при заряде <15% без зарядки
- `requirements.txt` — добавлен недостающий `google-generativeai`
- `Dockerfile`, `fly.toml`, `.github/workflows` — можно удалить, для телефона не нужны

## Установка на Narzo 50 (15 минут)

1. С F-Droid поставь: `Termux`, `Termux:Boot`, `Termux:API`.
2. В Termux:
```bash
pkg install -y git
git clone https://github.com/eminem0728/telegram-jarvis-bot.git ~/jarvis-bot
cd ~/jarvis-bot
chmod +x *.sh
./install.sh
```
3. Впиши токены:
```bash
nano .env
# TELEGRAM_TOKEN, OPENCODE_ZEN_API_KEY, AI_PROVIDER=opencode_zen
```
4. Запуск:
```bash
./start.sh
./status.sh
```
Выход из просмотра лога: `Ctrl+B`, потом `D`. Бот продолжает работать после выхода из Termux пока висит уведомление WakeLock.

5. Один раз настрой Realme, иначе убьёт фон:
   - удерживай Termux → Информация → Батарея → Без ограничений
   - разреши автозапуск и фоновую работу
   - в многозадачности закрепи Termux замком
   - Wi-Fi → оставаться подключённым в спящем режиме → всегда
   - открой приложение Termux:Boot один раз

## Команды

| Скрипт | Что делает |
|---|---|
| `./start.sh` | запуск в фоне (tmux + wake-lock) |
| `./stop.sh` | остановка |
| `./status.sh` | работает ли + хвост лога + батарея |
| `./logs.sh` | живой лог (`tail -f`) |
| `./update.sh` | `git pull` + переустановка + перезапуск |

После перезагрузки телефона бот стартует сам через `~/.termux/boot/boot-jarvis.sh`.

## Зарядка 24/7

- Ставь на слабую зарядку 5В/2А, не на родную 33Вт — меньше греется.
- Не клади под подушку / на солнце. Narzo 50 с 5000 мАч в простое жрёт мало, но `yt-dlp + ffmpeg` греют.
- Если бот молчит — сначала `./status.sh`, потом `./logs.sh`.
