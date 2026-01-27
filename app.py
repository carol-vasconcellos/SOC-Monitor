import logging
import requests
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os

# ================= CONFIG =================
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = Flask(__name__)

# Lista que armazena os alertas (histórico e estado atual)
alerts_history = []

# ================= LOG FORENSE =================
# O log registra tanto ataques quanto remediações para fins de auditoria
logging.basicConfig(
    filename="soc_audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

# ================= TELEGRAM =================
def send_telegram_alert(msg):
    if not TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": f"🚨 SOC ALERT\n{msg}"
        }, timeout=5)
    except Exception as e:
        print(f"Erro Telegram: {e}")

# ================= CORE SOC =================
def register_alert(alert_type, message, severity="MEDIUM"):
    alert = {
        "id": len(alerts_history) + 1,
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": alert_type,
        "severity": severity,
        "message": message,
        "status": "ACTIVE" # Todo alerta nasce como Ativo
    }
    # Insere no topo da lista para aparecer primeiro no dashboard
    alerts_history.insert(0, alert)

    log_msg = f"[{severity}] [{alert_type}] {message}"
    logging.info(log_msg)

    if severity in ["HIGH", "CRITICAL"]:
        send_telegram_alert(log_msg)

# ================= API DE ATAQUE =================
@app.route("/api/attack", methods=["POST"])
def receive_attack():
    data = request.get_json()
    attack_type = data.get("type")
    target = data.get("target", "cloud-app")

    if attack_type == "RANSOMWARE":
        register_alert("RANSOMWARE", f"Tentativa de criptografia no serviço {target}", "CRITICAL")

    elif attack_type == "FIM":
        register_alert("FILE INTEGRITY", f"Violação de integridade detectada em {target}", "HIGH")

    elif attack_type == "BRUTE_FORCE":
        register_alert("BRUTE FORCE", f"Múltiplas tentativas de login no serviço {target}", "HIGH")

    elif attack_type == "DDoS":
        register_alert("DDoS", f"Pico anormal de requisições no endpoint {target}", "CRITICAL")

    # Novo ataque de arquivo/exfiltração
    elif attack_type == "FILE_EXFILTRATION":
        register_alert("FILE_EXFIL", f"Upload/Exfiltração de arquivos sensíveis em {target}", "HIGH")

    else:
        register_alert("UNKNOWN", f"Evento suspeito recebido para {target}", "LOW")

    return jsonify({"status": "received", "type": attack_type})

# ================= API DE REMOÇÃO (REMEDIAÇÃO) =================
@app.route("/api/remediate", methods=["POST"])
def remediate():
    data = request.get_json()
    target_type = data.get("type")
    
    count = 0
    for alert in alerts_history:
        # Se encontrarmos alertas ativos do tipo especificado, "limpamos" eles
        if alert["type"] == target_type and alert["status"] == "ACTIVE":
            alert["status"] = "RESOLVED"
            alert["message"] += " -> [REMOVIDO/MITIGADO PELO SOC]"
            count += 1
    
    if count > 0:
        msg_rem = f"Remediação concluída: {count} ameaças de {target_type} neutralizadas."
        logging.info(f"[REMEDIATION] {msg_rem}")
        return jsonify({"status": "remediated", "count": count})
    
    return jsonify({"status": "no_active_threats_found"}), 404

# ================= DASHBOARD =================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/alerts")
def alerts():
    return jsonify(alerts_history)

# ================= MAIN =================
if __name__ == "__main__":
    # Rodando em 0.0.0.0 para permitir conexões externas se necessário
    app.run(host="0.0.0.0", port=5000, debug=True)