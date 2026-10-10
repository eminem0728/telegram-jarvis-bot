#!/data/data/com.termux/files/usr/bin/bash
# Живой лог
cd "$(dirname "$0")"
tail -f logs/bot.log
