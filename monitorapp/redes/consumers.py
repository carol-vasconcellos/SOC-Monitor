import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Rede, EventoRede, Intruso
from .utils import ping_rede, scan_portas
from django.utils import timezone

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('monitoramento_geral', self.channel_name)
        await self.accept()
        await self.enviar_estado_inicial()
        # Inicia a task que envia atualizações periódicas
        self.task = asyncio.create_task(self.enviar_atualizacao_periodica())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('monitoramento_geral', self.channel_name)
        self.task.cancel()

    async def enviar_estado_inicial(self):
        redes = await self.obter_status_redes()
        intrusos = await self.verificar_intrusos()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'redes': redes,
            'intrusos': intrusos
        }))

    async def obter_status_redes(self):
        redes_status = []
        redes = await sync_to_async(list)(Rede.objects.all())
        for rede in redes:
            status = await sync_to_async(ping_rede)(rede.ip_address)
            await sync_to_async(EventoRede.objects.create)(rede=rede, status=status)
            portas_abertas = await scan_portas(rede.ip_address)
            redes_status.append({
                'id': rede.id,
                'nome': rede.nome,
                'ip': rede.ip_address,
                'status': status,
                'ultima_verificacao': timezone.now().isoformat(),
                'portas_abertas': portas_abertas
            })
        return redes_status

    async def verificar_intrusos(self):
        # Implemente conforme seu modelo, aqui só exemplo vazio
        return []

    async def enviar_atualizacao_periodica(self):
        while True:
            redes = await self.obter_status_redes()
            await self.channel_layer.group_send(
                'monitoramento_geral',
                {
                    'type': 'atualizacao_rede',
                    'redes': redes
                }
            )
            await asyncio.sleep(10)  # a cada 10 segundos

    async def atualizacao_rede(self, event):
        redes = event['redes']
        await self.send(text_data=json.dumps({
            'type': 'network_update',
            'redes': redes,
        }))
