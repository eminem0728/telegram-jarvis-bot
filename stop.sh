#!/data/data/com.termux/files/usr/bin/bash
# Остановка бота
tmux kill-session -t jarvis 2>/dev/null && echo "Остановлен." || echo "Не был запущен."
termux-notification-remove 2>/dev/null || true
# wake-lock не снимаем специально — он нужен и другим задачам; снять вручную: termux-wake-unlock
