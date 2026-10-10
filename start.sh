#!/data/data/com.termux/files/usr/bin/bash
# Запуск бота в фоне (tmux + wake-lock + автоперезапуск при падении)
cd "$(dirname "$0")"

termux-wake-lock 2>/dev/null || true
mkdir -p data logs

if tmux has-session -t jarvis 2>/dev/null; then
  echo "Уже запущен. Подключиться: tmux attach -t jarvis"
  exit 0
fi

tmux new-session -d -s jarvis "while true; do python main.py 2>&1 | tee -a logs/bot.log; echo \"[crash] restart in 5s...\"; sleep 5; done"
termux-notification --title "Jarvis" --content "Бот запущен в фоне" 2>/dev/null || true

echo "Запущен. Лог: ./logs.sh или tmux attach -t jarvis"
echo "Остановка: ./stop.sh"
