from django.db import models

class Host(models.Model):
    nome = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(protocol='both')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.ip})"

class EventoPing(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    online = models.BooleanField()
    horario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "ONLINE" if self.online else "OFFLINE"
        return f"{self.host} - {status} em {self.horario}"
