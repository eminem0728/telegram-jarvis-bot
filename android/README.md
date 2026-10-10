# Jarvis Bot — отдельная APK (вариант 1, без Termux)

Python внутри приложения через Chaquopy + ForegroundService с кнопкой Вкл/Выкл.
Файл `main.py` подтягивается из корня репозитория автоматически при сборке
(`syncBotMain` в `app/build.gradle`), руками копировать не надо.

## Что нужно на ПК

- Android Studio (свежая, с bundled JDK 17), ~10 ГБ места
- Интернет на первой сборке: Gradle скачает Chaquopy + Python 3.11 + пакеты
- Телефон Narzo 50 с разрешением «установка из неизвестных источников»

## Сборка (первый раз минут 20-30)

1. В Android Studio: **Open** → выбери папку `android/` из репозитория.
2. Дождись **Gradle Sync** (полоска внизу). Первый раз долго — качается тулчейн
   Python 3.11 под arm64 и pip-пакеты:
   `python-telegram-bot`, `httpx`, `python-dotenv`, `pydub`,
   `SpeechRecognition`, `yt-dlp`. Всё чистый Python, собирается без ошибок.
3. Если Sync красный — `File → Sync Project with Gradle Files` ещё раз.
   Частые причины: нет интернета / нет места / старый кэш (`File → Invalidate Caches`).
4. **Build → Build APK(s)** → внизу появится путь:
   `app/build/outputs/apk/debug/app-debug.apk` (кнопка locate).
5. Скинь APK на телефон (USB / Telegram «Избранное») и поставь.

## Первый запуск на телефоне

1. Открой **Jarvis** → поля уже предзаполнены ключами со сборочной машины
   (`android/local.properties`, в GitHub не уходит) → просто жми
   **ВКЛЮЧИТЬ БОТА**. Если поля пустые — впиши вручную.
2. Разреши уведомления (иначе Android убьёт фон — это правило системы, не баг).
3. Удерживай иконку Jarvis → Информация → Батарея → **Без ограничений**,
   разреши автозапуск. В шторке должно висеть «Jarvis Bot работает».
4. После перезагрузки телефона бот стартует сам (`BootReceiver`),
   если был включён.

> Не раздавай свой APK кому попало: внутри зашиты твои ключи.

## Что работает из коробки, а что нет

- Чат с AI, погода, курс, картинки, поиск, скачивание видео/музыки,
  тегалки, память имён — всё работает.
- **ffmpeg**: для расшифровки голосовых и конвертации музыки в mp3 нужен
  бинарник. Без него:
  - музыка качается целым файлом как есть (m4a/webm),
  - видео качается целым mp4 без склейки,
  - голосовые отвечают «без ffmpeg не расшифрую».
- Если достанешь static-сборку `ffmpeg` под arm64 — положи файл с именем
  `ffmpeg` во внутреннюю папку данных приложения, `bot_main.py` сам
  добавит её в PATH и включит полный режим.

## Ручная проверка перед сборкой (на ПК)

```powershell
python -m py_compile ..\main.py
```

## Структура

- `app/src/main/java/com/jarvis/bot/MainActivity.kt` — экран: токены + Вкл/Выкл
- `app/src/main/java/com/jarvis/bot/JarvisService.kt` — ForegroundService:
  WakeLock + WifiLock, запуск Python в отдельном потоке, перезапуск при падении
- `app/src/main/java/com/jarvis/bot/BootReceiver.kt` — автозапуск после reboot
- `app/src/main/python/bot_main.py` — точка входа: папки данных, ffmpeg в PATH,
  импорт `main`, запуск `main()`
- `app/src/main/python/main.py` — НЕ коммитится (в `.gitignore`), генерируется
  из корня при каждой сборке
