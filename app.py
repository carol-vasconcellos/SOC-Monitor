import time
import hashlib
import requests
import logging
from threading import Thread
from datetime import datetime
from flask import Flask, render_template, jsonify, request, abort
import os, time, logging, hashlib
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

logging.basicConfig(filename='soc_audit.log', level=logging.INFO, 
                    format='%(asctime)s | %(message)s')

@app.before_request
def firewall_check():
    client_ip = request.remote_addr
    if client_ip in BANNED_IPS:
        return jsonify({"error": "IP BLOQUEADO PELO SOC", "reason": "Atividade Maliciosa Detectada"}), 403

def monitor_and_block_ip(ip):
    ATTACK_COUNTER[ip] = ATTACK_COUNTER.get(ip, 0) + 1
    if ATTACK_COUNTER[ip] >= 3:
        if ip not in BANNED_IPS:
            BANNED_IPS.add(ip)
            msg = f"🚫 FIREWALL: IP {ip} bloqueado após {ATTACK_COUNTER[ip]} tentativas de ataque."
           
            send_telegram_alert(msg)
            print(f"\n[!] {msg}\n")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"⚠️ SOC ALERT:\n{message}"}
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

@app.route('/api/inject', methods=['POST'])
def inject_alert():
    client_ip = request.remote_addr
    try:
        data = request.get_json()
        alert_type = data.get("type", "REMOTO")
        msg = data.get("message", "Alerta recebido")
        
        
        if alert_type in ["ATAQUE", "RANSOMWARE", "INFILTRAÇÃO"]:
            monitor_and_block_ip(client_ip)

        new_alert = {"time": datetime.now().strftime("%H:%M:%S"), "type": alert_type, "message": msg}
        
        alerts_history.insert(0, new_alert)
        
        return jsonify({"status": "success", "info": "SOC monitorando sua atividade"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

class DashboardHandler(FileSystemEventHandler):
    def __init__(self):
        self.hashes = {}

    def add_alert(self, type, msg):
        alert = {"time": datetime.now().strftime("%H:%M:%S"), "type": type, "message": msg}
        alerts_history.insert(0, alert) 
        logging.info(f"[{type}] {msg}")

    
    def on_created(self, event):
        if not event.is_directory:
            fname = os.path.basename(event.src_path)
            
            
            self.add_alert("INTRUSÃO", f"🚨 Ameaça detectada: {fname}. Analisando comportamento...")
            send_telegram_alert(f"🚨 INTRUSO DETECTADO: {fname}. Iniciando protocolo de expulsão!")

            
            time.sleep(1.5) 
            try:
                os.remove(event.src_path)
                
               
                msg_sucesso = f"🛡️ SISTEMA IMUNE: O arquivo {fname} foi destruído e o intruso expulso."
                self.add_alert("REMEDIAÇÃO", msg_sucesso)
                send_telegram_alert(f"✅ PROTOCOLO CONCLUÍDO: {fname} removido. Host limpo.")
                print(f"[SOC ACTIVE RESPONSE] {msg_sucesso}") 
            except Exception as e:
                self.add_alert("FALHA", f"❌ Falha ao expulsar intruso: {fname}")

    def on_modified(self, event):
        if not event.is_directory:
            new_hash = get_file_hash(event.src_path)
            if new_hash and new_hash != self.hashes.get(event.src_path):
                msg = f"Integridade Violada: {os.path.basename(event.src_path)}"
                self.add_alert("MODIFICAÇÃO", msg)
                send_telegram_alert(f"{msg}. Tentando reverter alteração...")
                
                self.hashes[event.src_path] = new_hash

    def on_deleted(self, event):
        self.add_alert("CRÍTICO", f"Arquivo Removido: {os.path.basename(event.src_path)}")

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/alerts')
def get_alerts(): 
    return jsonify(alerts_history)

@app.route('/api/reset_firewall')
def reset_firewall():
    BANNED_IPS.clear()
    ATTACK_COUNTER.clear()
    return "🛡️ Firewall Resetado! IPs liberados para novos testes.", 200

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