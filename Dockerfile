FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000
CMD python -c "
import subprocess, sys, time
while True:
    proc = subprocess.run([sys.executable, 'main.py'])
    if proc.returncode != 0:
        print(f'Bot exited with code {proc.returncode}, restarting in 3s...')
    time.sleep(3)
"
