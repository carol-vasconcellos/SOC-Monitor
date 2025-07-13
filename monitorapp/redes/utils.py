# redes/utils.py
import subprocess
import platform
import socket

def ping_rede(ip, port=53, timeout=2):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        subprocess.check_output(
            ['ping', param, '1', ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=5
        )
        return True
    except Exception:
        try:
            with socket.create_connection((ip, port), timeout):
                return True
        except Exception:
            return False

def bloquear_intruso(ip):
    try:
        if platform.system().lower() == 'windows':
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                'name=Bloqueio Intruso', 'dir=in', 'action=block',
                'remoteip=' + ip, 'enable=yes'
            ], check=True)
        else:
            subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], check=True)
            subprocess.run(['sudo', 'iptables-save'], check=True)
        return True
    except Exception as e:
        print(f"Erro ao bloquear IP {ip}: {e}")
        return False