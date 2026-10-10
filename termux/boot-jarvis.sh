#!/data/data/com.termux/files/usr/bin/bash
# Автозапуск после перезагрузки телефона. Копируется в ~/.termux/boot/ через install.sh
# Требуется приложение Termux:Boot из F-Droid.
termux-wake-lock
sleep 10
cd ~/jarvis-bot 2>/dev/null || cd $(dirname "$0")/../.. 2>/dev/null || exit 0
mkdir -p data logs
tmux kill-session -t jarvis 2>/dev/null || true
tmux new-session -d -s jarvis "while true; do python main.py 2>&1 | tee -a logs/bot.log; sleep 5; done"
