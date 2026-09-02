import argparse
import json
import os
from dataclasses import asdict
from net_sentinel.engine import ProbeEngine
from net_sentinel.adapter import AndroidAdapter

G, R, Y, C, B, RESET = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[1m', '\033[0m'

def main():
    parser = argparse.ArgumentParser(description="NetSentinel - Diagnóstico de Rede Android")
    parser.add_argument("domain", nargs="?", default="google.com", help="Domínio alvo")
    parser.add_argument("--json", action="store_true", help="Saída formatada em JSON")
    parser.add_argument("--fix", action="store_true", help="Executa rotina de reparo")
    
    args = parser.parse_args()
    engine = ProbeEngine(args.domain)
    res = engine.run()

    if args.json:
        print(json.dumps(asdict(res), indent=2))
        return

    print(f"\n{B}{C}=== NET-SENTINEL v3.0 ==={RESET}")
    print(f" Alvo:             {B}{res.target}{RESET}")
    print(f" Interface Ativa:  {res.interface}")
    print(f" Latência Teste:   {res.latency_ms} ms")
    print("-" * 40)
    
    print(f" DNS Direct (UDP):  {'['+G+'PASS'+RESET+']' if res.dns_udp_ok else '['+R+'FAIL'+RESET+']'}")
    print(f" OS Resolver (libc):{'['+G+'PASS'+RESET+']' if res.libc_dns_ok else '['+R+'FAIL'+RESET+']'}")
    print(f" Handshake TLS/SNI: {'['+G+'PASS'+RESET+']' if res.sni_tls_ok else '['+R+'FAIL'+RESET+']'}")
    print("-" * 40)

    if res.netd_bug_detected or args.fix:
        print(f"\n{Y}[*] Executando protocolo de auto-reparo...{RESET}")
        if res.resolved_ip:
            hosts_path = os.path.expanduser("~") + "/../usr/etc/hosts"
            try:
                with open(hosts_path, "a") as f:
                    f.write(f"\n{res.resolved_ip} {res.target} www.{res.target}\n")
                print(f"{G}[+] Rota aplicada na tabela do Termux.{RESET}")
            except Exception:
                pass

        if res.has_root:
            AndroidAdapter.force_root_netd_flush()
            AndroidAdapter.toggle_airplane_mode()
            print(f"{G}[+] Reset de rede e DNS efetuados via Root.{RESET}")
        else:
            AndroidAdapter.toggle_airplane_mode()
            print(f"\n{B}AÇÃO MANUAL NECESSÁRIA:{RESET}")
            print("1. Vá em Configurações > Rede e Internet > DNS Privado")
            print("2. Insira: dns.google")
            print("3. Reinicie o Wi-Fi para aplicar.")
    elif res.libc_dns_ok:
        print(f"{G}[SAUDÁVEL] A camada de rede está operando normalmente.{RESET}")
    else:
        print(f"{R}[BLOQUEIO] Falha geral de conexão na rede atual.{RESET}")

if __name__ == "__main__":
    main()
