#!/data/data/com.termux/files/usr/bin/bash
# Статус бота
cd "$(dirname "$0")"
if tmux has-session -t jarvis 2>/dev/null; then
  echo "STATUS: RUNNING (tmux jarvis)"
else
  echo "STATUS: STOPPED"
fi
echo "--- последние 20 строк лога ---"
tail -n 20 logs/bot.log 2>/dev/null || echo "(лог пока пуст)"
echo "--- батарея ---"
termux-battery-status 2>/dev/null || echo "(нужен termux-api)"
