from django.contrib import admin
from .models import Host, EventoPing

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ip', 'ativo')

@admin.register(EventoPing)
class EventoPingAdmin(admin.ModelAdmin):
    list_display = ('host', 'online', 'horario')
    list_filter = ('host', 'online')
