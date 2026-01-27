import time
import os
import random
import requests

# --- CONFIGURAÇÃO ---
RENDER_URL = "https://soc-monitor.onrender.com/api/inject" # Troque pela sua URL
TARGET_DIR = "./monitorar"

def notify_render(tipo, msg):
    try:
        requests.post(RENDER_URL, json={"type": tipo, "message": msg}, timeout=5)
    except:
        print("[!] Falha ao notificar o dashboard remoto.")

def simulate_advanced_attack():
    if not os.path.exists(TARGET_DIR): os.makedirs(TARGET_DIR)
    
    print("[*] Iniciando ataque híbrido (Local + Nuvem)...")
    
    # FASE 1
    for i in range(2):
        filename = f"malware_{i}.exe"
        with open(os.path.join(TARGET_DIR, filename), "w") as f: f.write("virus")
        notify_render("INFILTRAÇÃO", f"Payload implantado: {filename}")
        time.sleep(2)

    # FASE 2
    notify_render("RANSOMWARE", "Criptografia em massa iniciada no host local.")
    time.sleep(2)

    # FASE 3
    notify_render("LIMPEZA", "Removendo rastros e logs do sistema.")
    print("[OK] Ataque concluído e Dashboard notificado.")

if __name__ == "__main__":
    simulate_advanced_attack()