import time
import hashlib
import requests
import logging
import os
from threading import Thread
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TARGET_DIR = "./monitorar"

BANNED_IPS = set()
ATTACK_COUNTER = {}

app = Flask(__name__)
alerts_history = [] 

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) 

logging.basicConfig(
    filename='soc_audit.log', 
    level=logging.INFO, 
    format='%(message)s', 
    encoding='utf-8'
)

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"⚠️ SOC ALERT:\n{message}"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        pass 

def add_full_alert(alert_type, message):
   
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    clean_msg = f"[{timestamp}] {alert_type}: {message}"
    
    alert_entry = {
        "time": timestamp, 
        "type": alert_type, 
        "message": message
    }
    alerts_history.insert(0, alert_entry)
    
    logging.info(clean_msg)
    
    send_telegram_alert(clean_msg)
    
    print(f"SOC ACTION -> {clean_msg}")

@app.before_request
def firewall_check():
    client_ip = request.remote_addr
    if request.path == '/api/reset_firewall':
        return None 
    if client_ip in BANNED_IPS:
        return jsonify({"error": "IP BLOQUEADO PELO SOC", "reason": "Atividade Maliciosa Detectada"}), 403

def monitor_and_block_ip(ip):
    ATTACK_COUNTER[ip] = ATTACK_COUNTER.get(ip, 0) + 1
    if ATTACK_COUNTER[ip] >= 3:
        if ip not in BANNED_IPS:
            BANNED_IPS.add(ip)
            msg = f"🚫 FIREWALL: IP {ip} BANIDO após {ATTACK_COUNTER[ip]} ataques."
            add_full_alert("FIREWALL", msg)

def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except:
        return None

@app.route('/api/inject', methods=['POST'])
def inject_alert():
    client_ip = request.remote_addr
    try:
        data = request.get_json()
        alert_type = data.get("type", "REMOTO")
        msg = data.get("message", "Alerta recebido via API")
        
        if alert_type in ["ATAQUE", "RANSOMWARE", "INFILTRAÇÃO"]:
            monitor_and_block_ip(client_ip)

        add_full_alert(alert_type, msg)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

class DashboardHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            fname = os.path.basename(event.src_path)
            add_full_alert("INTRUSÃO", f"🚨 Ameaça detectada: {fname}")
            
            time.sleep(1.5) 
            try:
                os.remove(event.src_path)
                add_full_alert("REMEDIAÇÃO", f"🛡️ Expulsão concluída: {fname} removido.")
            except:
                add_full_alert("FALHA", f"Não foi possível remover {fname}")

    def on_modified(self, event):
        if not event.is_directory:
            add_full_alert("MODIFICAÇÃO", f"Arquivo alterado: {os.path.basename(event.src_path)}")

@app.route('/api/logs')
def get_logs():
    try:
        if os.path.exists('soc_audit.log'):
            with open('soc_audit.log', 'r', encoding='utf-8', errors='replace') as f:
                logs = f.readlines()
                
                return jsonify([line.strip() for line in logs[-20:] if line.strip()])
        return jsonify(["[SISTEMA] Aguardando eventos maliciosos..."])
    except Exception as e:
        return jsonify([f"Erro ao ler logs: {str(e)}"])

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/alerts')
def get_alerts(): return jsonify(alerts_history)

@app.route('/api/reset_firewall')
def reset_firewall():
    BANNED_IPS.clear()
    ATTACK_COUNTER.clear()
    return "🛡️ Firewall Resetado! IPs liberados.", 200

def run_monitor():
    if not os.path.exists(TARGET_DIR): os.makedirs(TARGET_DIR)
    event_handler = DashboardHandler()
    observer = Observer()
    observer.schedule(event_handler, TARGET_DIR, recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except: observer.stop()

if __name__ == "__main__":
    monitor_thread = Thread(target=run_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    app.run(host="0.0.0.0", port=5000)