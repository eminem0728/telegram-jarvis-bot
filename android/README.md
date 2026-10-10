# Jarvis Bot — Android APK (standalone, для Realme Narzo 50)

Отдельное приложение без Termux. Python внутри через Chaquopy + ForegroundService.

## Как собрать APK

1. Поставь Android Studio (на ПК).
2. Открой папку `android/` из этого репозитория как проект.
3. Дождись sync Gradle (скачается Chaquopy + Python 3.11).
4. Build -> Build APK(s). Получишь `app-debug.apk`.
5. Скинь на Narzo 50, разреши «установку из неизвестных источников», поставь.
6. Открой Jarvis -> вставь `TELEGRAM_TOKEN` и `OPENCODE_ZEN_API_KEY` -> кнопка ВКЛ.
7. Разреши: уведомления + «без ограничений» в батарее + автозапуск.
   На Realme: удерживай иконку Jarvis -> Информация -> Батарея -> Без ограничений.

## Как это работает

- `MainActivity.kt` — экран с большой кнопкой Вкл/Выкл + поля для ключей + лог.
- `JarvisService.kt` — ForegroundService с постоянным уведомлением, WakeLock + WifiLock, перезапуск при падении. Внутри запускает Python `bot_main.start_bot()`.
- `BootReceiver.kt` — автозапуск после перезагрузки телефона.
- `bot_main.py` — копия `main.py`, но без health-сервера (на телефоне не нужен) и с путями в `filesDir`.

Без уведомления в шторке на Android 12+ фон убивается — это ограничение Android, а не баг. Уведомление «Jarvis работает» должно висеть всегда.

## Важно

- Размер APK ~70-120МБ (внутри Python + yt-dlp + openai + telegram).
- Музыка/видео через ffmpeg: используется `mobile-ffmpeg`, на Helio G96 работает.
- Если бот падает — смотри лог прямо в приложении.
