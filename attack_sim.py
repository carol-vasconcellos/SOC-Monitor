import time
import os
import requests

# CONFIGURAÇÃO
RENDER_URL = "https://soc-monitor.onrender.com/api/inject" 
TARGET_DIR = "./monitorar"

def notify_render(tipo, msg):
    try:
        requests.post(RENDER_URL, json={"type": tipo, "message": msg}, timeout=5)
    except:
        print("[!] Erro de conexão com o servidor.")

def simulate_attack():
    if not os.path.exists(TARGET_DIR): os.makedirs(TARGET_DIR)
    
    print("-" * 50)
    print("[*] INICIANDO ATAQUE: INJETANDO MALWARES")
    print("-" * 50)
    
    # O ataque apenas planta os arquivos
    for i in range(3):
        filename = f"virus_payload_{i}.exe"
        path = os.path.join(TARGET_DIR, filename)
        
        with open(path, "w") as f:
            f.write("payload_malicioso_12345")
        
        print(f"[+] Injetado: {filename}")
        notify_render("ATAQUE", f"Tentativa de infiltração: {filename}")
        
        # Espera um pouco para ver o SOC agir no terminal ao lado
        time.sleep(3)

    print("\n[*] Fim do ataque. Se o SOC estiver rodando, os arquivos acima já foram deletados por ele.")
    print("-" * 50)

if __name__ == "__main__":
    simulate_attack()