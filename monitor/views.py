from django.shortcuts import render
from .models import Host, EventoPing
from django.utils.timezone import now, timedelta

def dashboard(request):
    hosts = Host.objects.all()
    status = {}
    historico = {}
    for host in hosts:
        ultimo = EventoPing.objects.filter(host=host).order_by('-horario').first()
        status[host] = ultimo.online if ultimo else False
        historico[host.nome] = EventoPing.objects.filter(host=host, horario__gte=now()-timedelta(hours=12))
    return render(request, "monitor/dashboard.html", {"status": status, "historico": historico})
