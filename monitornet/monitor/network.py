import psutil
import time

# Simples histórico para detectar picos de tráfego
history = []

def get_network_data():
    net = psutil.net_io_counters()
    data = {
        'bytes_sent': net.bytes_sent,
        'bytes_recv': net.bytes_recv,
        'packets_sent': net.packets_sent,
        'packets_recv': net.packets_recv,
    }
    history.append((time.time(), net.bytes_recv + net.bytes_sent))
    return data

def detect_ddos():
    now = time.time()
    recent = [val for ts, val in history if now - ts < 10]
    if len(recent) >= 2 and (max(recent) - min(recent)) > 10000000:  # 10 MB em 10s
        return True
    return False
