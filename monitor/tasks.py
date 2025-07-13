from celery import shared_task
from ping3 import ping
from .models import Host, EventoPing

@shared_task
def verificar_hosts():
    hosts = Host.objects.filter(ativo=True)
    for host in hosts:
        try:
            resultado = ping(host.ip, timeout=2)
            online = resultado is not None
            ultimo = EventoPing.objects.filter(host=host).order_by('-horario').first()
            if not ultimo or ultimo.online != online:
                EventoPing.objects.create(host=host, online=online)
        except:
            EventoPing.objects.create(host=host, online=False)
