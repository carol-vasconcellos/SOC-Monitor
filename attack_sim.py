import time
import os
import random
import requests

# --- CONFIGURAÇÃO (Troque pela sua URL real do Render) ---
RENDER_URL = "https://soc-monitor.onrender.com/api/inject" 
TARGET_DIR = "./monitorar"

def notify_render(tipo, msg):
    try:
        # Envia o alerta para o Dashboard na Nuvem
        requests.post(RENDER_URL, json={"type": tipo, "message": msg}, timeout=5)
    except Exception as e:
        print(f"[!] Erro ao notificar Render: {e}")

def simulate_advanced_attack():
    if not os.path.exists(TARGET_DIR): os.makedirs(TARGET_DIR)
    
    print("-" * 50)
    print("[*] INICIANDO ATAQUE HÍBRIDO: LOCAL -> RENDER")
    print("-" * 50)
    
    # FASE 1: Infiltração (Criação de arquivos)
    created_files = []
    for i in range(2):
        filename = f"malware_detectado_{i}.exe"
        path = os.path.join(TARGET_DIR, filename)
        with open(path, "w") as f: f.write("conteudo_malicioso_simulado")
        created_files.append(path)
        
        print(f"[+] Criando: {filename}")
        notify_render("INFILTRAÇÃO", f"Arquivo suspeito plantado: {filename}")
        time.sleep(2)

    # FASE 2: Ransomware (Modificação)
    print("[!] Simulando criptografia de arquivos...")
    notify_render("RANSOMWARE", "Atividade de criptografia detectada no host local.")
    time.sleep(2)

    # FASE 3: LIMPEZA REAL (Apaga os arquivos da pasta)
    print("[*] Fase de Limpeza: Removendo evidências locais...")
    for path in created_files:
        if os.path.exists(path):
            os.remove(path)
            print(f"[-] Removido: {os.path.basename(path)}")
    
    notify_render("LIMPEZA", "Ataque finalizado. Rastros removidos da máquina alvo.")
    print("-" * 50)
    print("[OK] Sucesso! Verifique seu Dashboard e o Telegram.")

if __name__ == "__main__":
    simulate_advanced_attack()