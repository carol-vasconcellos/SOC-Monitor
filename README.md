# SOC File Integrity Monitor (FIM) com Python

Este projeto simula uma função crítica de um SOC (Security Operations Center): o monitoramento de integridade de arquivos em tempo real.

## 🚀 Funcionalidades
* **Monitoramento em Tempo Real:** Detecta criação, modificação e deleção de arquivos usando a biblioteca `watchdog`.
* **Análise de Integridade (Hashing):** Utiliza o algoritmo **SHA-256** para validar se o conteúdo do arquivo foi alterado, evitando falsos positivos.
* **Alertas Automatizados:** Integração com a API do **Telegram** para notificações instantâneas de incidentes.

## 🛠️ Tecnologias
* Python 3.x
* Bibliotecas: `hashlib`, `requests`, `python-dotenv`, `watchdog`

## 🛡️ Como o projeto demonstra habilidades de SOC N1?
Este projeto cobre o ciclo fundamental de resposta a incidentes:
1. **Detecção:** Monitoramento contínuo de diretórios críticos.
2. **Análise:** Comparação de hashes para confirmar alterações maliciosas.
3. **Notificação:** Reporte imediato para o analista via canal de comunicação externo.