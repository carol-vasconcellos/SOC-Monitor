# 🛡️ SOC File Integrity Monitor (FIM) & Dashboard

Este projeto simula uma operação real de um **SOC (Security Operations Center)** focado em **Monitoramento de Integridade de Arquivos (FIM)**. Ele utiliza Python para detectar alterações em ativos críticos em tempo real, valida a integridade via criptografia (Hashes) e notifica o analista através de um Dashboard Web e alertas no Telegram.

## 📋 O que aconteceu? (Arquitetura do Projeto)

O projeto evoluiu de um script simples para uma solução completa de monitoramento:

1. **Monitoramento Ativo:** Utilizamos a biblioteca `watchdog` para "vigiar" a pasta `./monitorar` através de APIs nativas do sistema operacional (Windows).
2. **Validação por Hash (SHA-256):** Para evitar falsos positivos, o sistema gera uma "impressão digital" única para cada arquivo. Se o conteúdo mudar, o Hash muda, e o SOC detecta a violação de integridade. 3.  **Notificação e Resposta:** Ao detectar um incidente, o sistema executa duas ações:
* Envia um alerta instantâneo via **Telegram Bot API**.
* Registra o evento no **Dashboard Web** (Flask) para visualização centralizada.


3. **Simulação de Ataque:** Criamos um script que simula o comportamento de um **Ransomware**, realizando criptografia (modificação em massa) e limpeza de evidências (deleção).

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework Web:** Flask (Dashboard)
* **Bibliotecas:** `watchdog` (Monitoramento), `requests` (API Telegram), `hashlib` (Criptografia), `python-dotenv` (Segurança).

## 📂 Estrutura do Repositório

* `app.py`: O "coração" do SOC. Roda o monitoramento e o servidor do Dashboard.
* `attack_sim.py`: Script de Red Team para testar as defesas.
* `templates/index.html`: Interface visual do analista SOC.
* `.env`: Armazena credenciais sensíveis (Token e Chat ID).
* `soc_audit.log`: Arquivo de auditoria forense para registro persistente de todos os eventos.

## 🛠️ Como Executar

1. **Prepare o Ambiente Virtual:**
```bash
python -m venv .venv
.venv\Scripts\activate

```


2. **Instale as Dependências:**
```bash
pip install -r requirements.txt

```


3. **Configure suas Credenciais:**
Crie um arquivo `.env` com seu `TELEGRAM_TOKEN` e `TELEGRAM_CHAT_ID`.
4. **Inicie o SOC:**
```bash
python app.py

```


5. **Simule um Incidente:**
Em outro terminal, execute:
```bash
python attack_sim.py

```



## 🛡️ Demonstração de Habilidades (SOC N1 / Engenharia de Redes)

Este projeto demonstra competência em:

* **Automação de Segurança:** Substituição de tarefas manuais por scripts Python.
* **Cibersegurança Prática:** Entendimento de Hashes, criptografia e vetores de ataque (Ransomware).
* **Integração de APIs:** Comunicação entre sistemas de monitoramento e ferramentas de mensageria.
* **Resposta a Incidentes:** Criação de logs de auditoria e Dashboards de visibilidade.
