from django.shortcuts import render
from .network import get_network_data, detect_ddos

def dashboard(request):
    network_data = get_network_data()
    ddos_detected = detect_ddos()
    network_data['ddos_detected'] = ddos_detected
    return render(request, 'monitor/dashboard.html', network_data)
