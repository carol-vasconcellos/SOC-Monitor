import time
import requests
import random

SOC_URL = "https://soc-monitor.onrender.com/api/inject"

import time
import requests

SOC_URL = "https://soc-monitor.onrender.com/api/attack"
REMEDIATE_URL = "https://soc-monitor.onrender.com/api/remediate"

def trigger(tipo, alvo):
    requests.post(SOC_URL, json={"type": tipo, "target": alvo})
    print(f"[!] Ataque {tipo} enviado.")

def clear(tipo):
    requests.post(REMEDIATE_URL, json={"type": tipo})
    print(f"[✔] SOC executou remoção de: {tipo}")

# --- Simulação ---
trigger("DDoS", "LoadBalancer-Main")
time.sleep(1)
trigger("FILE_EXFILTRATION", "/data/customers.db")
time.sleep(2)

print("\n--- SOC Iniciando Resposta Automática ---")
clear("DDoS")
time.sleep(1)
clear("FILE_EXFILTRATION")