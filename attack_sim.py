import time
import os
import random

TARGET_DIR = "./monitorar"

def simulate_advanced_attack():
    print(f"[*] ALVO DETECTADO: {os.path.abspath(TARGET_DIR)}")
    print("[!] Iniciando sequência de ataque em 5 segundos...")
    time.sleep(5)

    print("\n[FASE 1] Infiltração: Plantando backdoors...")
    for i in range(3):
        filename = os.path.join(TARGET_DIR, f"sys_config_{i}.bat")
        with open(filename, "w") as f:
            f.write("@echo off\necho Infiltrado!")
        print(f"[+] Backdoor criado: {filename}")
        time.sleep(1)

    print("\n[FASE 2] Ransomware: Criptografando arquivos críticos...")
    files = [f for f in os.listdir(TARGET_DIR) if os.path.isfile(os.path.join(TARGET_DIR, f))]
    for file in files:
        path = os.path.join(TARGET_DIR, file)
        with open(path, "a") as f:
            f.write(f"\nENCRYPTED_BY_SOC_TEST_{random.randint(1000, 9999)}")
        print(f"[!] Integridade violada: {file} (Hash alterado)")
        time.sleep(1.5)

    print("\n[FASE 3] Limpeza: Removendo evidências do ataque...")
    time.sleep(2)
    for file in files:
        path = os.path.join(TARGET_DIR, file)
        os.remove(path)
        print(f"[-] Evidência deletada: {file}")
        time.sleep(0.5)

    print("\n[COMPLETO] O SOC deve ter detectado múltiplas violações e enviado alertas.")

if __name__ == "__main__":
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    simulate_advanced_attack()