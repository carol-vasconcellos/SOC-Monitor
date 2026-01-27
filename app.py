import time
import hashlib
import requests
import os
import logging
from threading import Thread
from datetime import datetime
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = Flask(__name__)
alerts_history = [] 

logging.basicConfig(filename='soc_audit.log', level=logging.INFO, 
                    format='%(asctime)s | %(message)s')

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"⚠️ SOC DASHBOARD ALERT:\n{message}"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        logging.error(f"Erro Telegram: {e}")

def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except:
        return None

class DashboardHandler(FileSystemEventHandler):
    def __init__(self):
        self.hashes = {}

    def add_alert(self, type, msg):
        alert = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": type,
            "message": msg
        }
        alerts_history.insert(0, alert) 
        logging.info(f"[{type}] {msg}")

    def on_modified(self, event):
        if not event.is_directory:
            new_hash = get_file_hash(event.src_path)
            if new_hash and new_hash != self.hashes.get(event.src_path):
                msg = f"Integridade Violada: {os.path.basename(event.src_path)}"
                self.add_alert("MODIFICAÇÃO", msg)
                send_telegram_alert(msg)
                self.hashes[event.src_path] = new_hash

    def on_deleted(self, event):
        msg = f"Arquivo Removido: {os.path.basename(event.src_path)}"
        self.add_alert("CRÍTICO", msg)
        send_telegram_alert(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alerts')
def get_alerts():
    return jsonify(alerts_history)

def run_monitor():
    path = "./monitorar"
    if not os.path.exists(path): os.makedirs(path)
    event_handler = DashboardHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except: observer.stop()

if __name__ == "__main__":

    monitor_thread = Thread(target=run_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    app.run(debug=False, port=5000)