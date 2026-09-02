# 📡 NetSentinel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Termux-brightgreen.svg)](https://termux.dev/)

> **NetSentinel** é um framework profissional de diagnóstico de rede e auto-reparo (auto-healing) para Android via Termux. Ele identifica falhas silenciosas na pilha de rede do sistema operacional (`netd` / `libc`) e restaura a conectividade automaticamente.

---

## 📑 Sumário
- [Por que o NetSentinel?](#-por-que-o-netsentinel)
- [Funcionalidades](#-funcionalidades)
- [Instalação Rápida (1-Click)](#-instalação-rápida-1-click)
- [Como Usar](#-como-usar)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Licença](#-licença)

---

## 🎯 Por que o NetSentinel?

Em várias versões do Android, o daemon de rede (`netd`) pode entrar em um estado de travamento parcial:
1. Os pacotes de rede continuam trafegando normalmente.
2. A resolução de DNS via chamadas de sistema (`libc` / `getaddrinfo`) falha para os aplicativos.
3. Testes simples de `ping` continuam reportando falso-positivo.

O **NetSentinel** realiza diagnósticos isolados em 3 camadas e aplica rotinas de reparo locais (no Termux) e no nível do sistema operacional (caso possua acesso Root).

---

## 🚀 Funcionalidades

- 🔬 **Sonda Tripla de Conectividade:**
  - **DNS Direct (UDP):** Valida se o servidor DNS da operadora/Wi-Fi responde na porta 53.
  - **OS Resolver (`libc`):** Testa se a API nativa do Android está resolvendo nomes para os apps.
  - **Handshake TLS/SNI:** Valida o transporte físico e rotas HTTPS forçando IP no cabeçalho SNI.
- 🛠️ **Protocolo de Auto-Reparo (`--fix`):**
  - Injeção de rotas locais no `/etc/hosts` do Termux.
  - Limpeza de tabelas `ndc` e renovação de DNS Privado (em dispositivos com Root).
  - Ciclo de reinicialização de interface via modo avião nativo.
- 🤖 **Modo Automação (`--json`):** Exporta o estado exato da rede em JSON formatado para integração com scripts ou Tasker.

---

## 📦 Instalação Rápida (1-Click)

Cole o comando abaixo no terminal do seu Termux:

```bash
curl -sL [https://raw.githubusercontent.com/luanleal180398/net-sentinel/main/install.sh](https://raw.githubusercontent.com/luanleal180398/net-sentinel/main/install.sh) | bash
