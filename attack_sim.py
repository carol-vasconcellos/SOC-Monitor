import time
import os
import requests


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
    
    
    for i in range(3):
        filename = f"virus_payload_{i}.exe"
        path = os.path.join(TARGET_DIR, filename)
        
        with open(path, "w") as f:
            f.write("payload_malicioso_12345")
        
        print(f"[+] Injetado: {filename}")
        notify_render("ATAQUE", f"Tentativa de infiltração: {filename}")
        
        time.sleep(3)

    print("\n[*] Fim do ataque. Se o SOC estiver rodando, os arquivos acima já foram deletados por ele.")
    print("-" * 50)
    
def simulate_aggressive_attack():
    print("🚀 Iniciando sequência de ataques...")
    
    for i in range(1, 6):
        print(f"\n[#] Tentativa {i}: Enviando payload malicioso...")
        try:
            response = requests.post(RENDER_URL, json={
                "type": "ATAQUE",
                "message": f"Injeção de código tentativa {i}"
            }, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Ataque enviado (Servidor ainda processando...)")
            elif response.status_code == 403:
                print(f"❌ FALHA CRÍTICA: O SOC nos detectou! IP Bloqueado.")
                print(f"Mensagem do Servidor: {response.json().get('error')}")
                break # Sai do loop pois foi expulso
                
        except Exception as e:
            print(f"Erro de conexão: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    simulate_attack()
    simulate_aggressive_attack()