# redes/views.py
from django.shortcuts import render
from .models import Rede, EventoRede, Intruso, RegraBloqueio
from .utils import ping_rede, bloquear_intruso
import ipaddress

def detectar_intrusos(rede):
    ips_conhecidos = [r.ip_address for r in Rede.objects.all()]
    intrusos_detectados = []
    
    for ip in ips_conhecidos:
        rede_ip = ipaddress.ip_network(ip, strict=False)
        if not any(str(ip) in ips_conhecidos for ip in rede_ip.hosts()):
            intruso, criado = Intruso.objects.get_or_create(
                ip_address=ip,
                defaults={'tentativas': 1}
            )
            if not criado:
                intruso.tentativas += 1
                intruso.save()
            intrusos_detectados.append(intruso)
    
    return intrusos_detectados

def monitor_redes(request):
    redes = Rede.objects.all()
    resultados = []
    intrusos = []

    for rede in redes:
        status = ping_rede(rede.ip_address)
        EventoRede.objects.create(rede=rede, status=status)
        resultados.append({'rede': rede, 'status': status})
        
        intrusos_rede = detectar_intrusos(rede)
        intrusos.extend(intrusos_rede)
        
        try:
            regra = RegraBloqueio.objects.get(rede=rede)
            for intruso in intrusos_rede:
                if intruso.tentativas >= regra.limite_tentativas and not intruso.bloqueado:
                    if regra.acao == 'block':
                        if bloquear_intruso(intruso.ip_address):
                            intruso.bloqueado = True
                            intruso.save()
        except RegraBloqueio.DoesNotExist:
            pass

    data_grafico = {rede.nome: EventoRede.objects.filter(rede=rede, status=False).count() for rede in redes}

    return render(request, 'monitor.html', {
        'resultados': resultados,
        'data_grafico': data_grafico,
        'intrusos': intrusos,
        'websocket_url': 'ws://' + request.get_host() + '/ws/status/'
    })