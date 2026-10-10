"""Точка входа для APK. Рядом должен лежать main.py (скопирован из корня репо)."""
import os
import sys

def start_bot(base_dir: str, token: str, zen_key: str):
    os.makedirs(base_dir, exist_ok=True)
    os.chdir(base_dir)

    os.environ["TELEGRAM_TOKEN"] = token or ""
    if zen_key:
        os.environ["OPENCODE_ZEN_API_KEY"] = zen_key
    os.environ.setdefault("AI_PROVIDER", "opencode_zen")

    # python-исходники Chaquopy лежат в sys.path; main.py кладем рядом с этим файлом
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)

    # Отключаем health-сервер на телефоне (не нужен, только жрет батарею):
    # в main.py run_health_server запускается из main(), поэтому глушим PORT
    # и подменяем функцию до импорта.
    import main as bot
    bot.run_health_server = lambda: None

    # Убираем оригинальный threading health-сервер из main() monkey-патчем:
    # main.main() сам создаст Application и уйдет в run_polling (блокирующий) — это то что надо,
    # он работает в потоке JarvisService, не в UI.
    bot.main()
