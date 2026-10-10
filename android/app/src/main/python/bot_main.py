"""Точка входа для APK. main.py подкладывается рядом при сборке (syncBotMain)."""
import os
import sys


def start_bot(base_dir: str, token: str, ai_key: str):
    data_dir = os.path.join(base_dir, "data")
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    # Папки данных ДО импорта main (иначе возьмёт свои рядом с кодом).
    os.environ["JARVIS_DATA_DIR"] = data_dir
    os.environ["JARVIS_LOG_DIR"] = logs_dir
    os.environ["PHONE_MODE"] = "1"

    os.environ["TELEGRAM_TOKEN"] = token or ""
    # Ключ Zen начинается с sk-, ключ Gemini (AI Studio) — иначе.
    if (ai_key or "").startswith("sk-"):
        os.environ["AI_PROVIDER"] = "opencode_zen"
        os.environ["OPENCODE_ZEN_API_KEY"] = ai_key
    else:
        os.environ["AI_PROVIDER"] = "gemini"
        if ai_key:
            os.environ["GEMINI_API_KEY"] = ai_key

    # ffmpeg: pydub и yt-dlp ищут БИНАРНИК в PATH. Если пользователь положил
    # static-сборку arm64 в filesDir/ffmpeg — подсовываем её первой.
    ffmpeg_bin = os.path.join(base_dir, "ffmpeg")
    if os.path.isfile(ffmpeg_bin):
        try:
            os.chmod(ffmpeg_bin, 0o755)
        except Exception:
            pass
        os.environ["PATH"] = base_dir + os.pathsep + os.environ.get("PATH", "")
        os.environ["FFMPEG_BINARY"] = ffmpeg_bin

    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)

    os.chdir(base_dir)

    import main as bot
    bot.main()
