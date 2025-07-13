from django.db import models
from django.utils import timezone

class Rede(models.Model):
    nome = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    mascara = models.CharField(max_length=15, default='255.255.255.0')
    gateway = models.GenericIPAddressField(blank=True, null=True)
    intervalo_verificacao = models.IntegerField(default=60)  # segundos
    dispositivos_autorizados = models.JSONField(default=list)

    def __str__(self):
        return f"{self.nome} ({self.ip_address})"

class EventoRede(models.Model):
    rede = models.ForeignKey(Rede, on_delete=models.CASCADE)
    status = models.BooleanField()
    latencia = models.FloatField(null=True, blank=True)
    portas_abertas = models.JSONField(default=list)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['rede', 'status']),
        ]

class Intruso(models.Model):
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    primeira_deteccao = models.DateTimeField(auto_now_add=True)
    ultima_tentativa = models.DateTimeField(auto_now=True)
    tentativas = models.PositiveIntegerField(default=1)
    bloqueado = models.BooleanField(default=False)
    motivo = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Intrusos"
        ordering = ['-ultima_tentativa']

    def bloquear(self):
        from .utils import bloquear_ip
        if bloquear_ip(self.ip_address):
            self.bloqueado = True
            self.save()
            return True
        return False

from django.utils import timezone

class RegraBloqueio(models.Model):
    rede = models.ForeignKey(Rede, on_delete=models.CASCADE)
    limite_tentativas = models.PositiveIntegerField(default=3)
    acao = models.CharField(
        max_length=10,
        choices=[('alert', 'Alerta'), ('block', 'Bloquear')],
        default='alert'
    )
    ip = models.GenericIPAddressField(default='127.0.0.1')
    porta = models.PositiveIntegerField(null=True, blank=True)
    protocolo = models.CharField(max_length=10, choices=[("TCP", "TCP"), ("UDP", "UDP")], default="TCP")
    motivo = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Regra de Bloqueio"
        verbose_name_plural = "Regras de Bloqueio"

    def __str__(self):
        return f"{self.ip}:{self.porta} ({self.protocolo}) - {self.rede}"


