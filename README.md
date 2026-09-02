# 📡 NetSentinel v3.0

Ferramenta CLI para diagnóstico avançado de rede e auto-reparo de falhas de resolução DNS/`netd` em dispositivos Android via Termux.

## 🚀 Funcionalidades

- **Diagnóstico Triplo:** Avalia DNS direto (UDP), Resolvedor nativo do SO (`libc`) e *handshake* TLS via SNI.
- **Auto-Reparo:**
  - Aplica entradas diretas na tabela `/etc/hosts` do Termux.
  - Executa flush e redefinição do serviço `netd` (para aparelhos com Root).
  - Executa ciclo automático de rede via modo avião.
- **Integração:** Saída formatada em texto colorido ou objeto estruturado JSON (`--json`).

## 📦 Instalação (1-Click)

Rode o comando abaixo dentro do Termux:

```bash
curl -sL [https://raw.githubusercontent.com/SEU_USUARIO/net-sentinel/main/install.sh](https://raw.githubusercontent.com/SEU_USUARIO/net-sentinel/main/install.sh) | bash
