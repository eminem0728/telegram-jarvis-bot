#!/data/data/com.termux/files/usr/bin/bash
# Установка Джарвиса на телефон (Realme Narzo 50 и любой Android с Termux)
set -e
echo "== Jarvis install =="

pkg update -y
pkg upgrade -y
pkg install -y python ffmpeg git tmux termux-api openssh

# проект уже должен лежать в ~/jarvis-bot (git clone) — если скрипт запущен оттуда, просто продолжаем
# В Termux системный pip защищён (PEP 668): `pip install --upgrade pip` запрещён,
# пакеты ставим с --break-system-packages. Телефон single-purpose, это ок.
pip install --break-system-packages -r requirements.txt

mkdir -p data logs

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Создан .env из примера — впиши туда TELEGRAM_TOKEN и OPENCODE_ZEN_API_KEY:"
  echo "  nano .env"
else
  echo ".env уже есть, не трогаю."
fi

# автозапуск после перезагрузки (нужен Termux:Boot из F-Droid)
mkdir -p ~/.termux/boot
cp -f termux/boot-jarvis.sh ~/.termux/boot/boot-jarvis.sh
chmod +x ~/.termux/boot/boot-jarvis.sh

echo ""
echo "Готово. Дальше:"
echo "  1) nano .env  — впиши токены"
echo "  2) ./start.sh — запуск"
echo "  3) Открой Termux:Boot один раз и разреши автозапуск"
