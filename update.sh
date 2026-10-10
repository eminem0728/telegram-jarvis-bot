#!/data/data/com.termux/files/usr/bin/bash
# Обновление бота с гитхаба
cd "$(dirname "$0")"
./stop.sh 2>/dev/null || true
git pull
pip install -r requirements.txt
./start.sh
