import subprocess
import socket
import time
import re
from dataclasses import dataclass
from typing import Optional
from net_sentinel.adapter import AndroidAdapter

@dataclass
class DiagnosticResult:
    target: str
    interface: str
    dns_udp_ok: bool
    libc_dns_ok: bool
    sni_tls_ok: bool
    resolved_ip: Optional[str]
    netd_bug_detected: bool
    has_root: bool
    latency_ms: float

class ProbeEngine:
    def __init__(self, target: str):
        self.target = self._sanitize(target)

    @staticmethod
    def _sanitize(url: str) -> str:
        url = re.sub(r'^https?://', '', url, flags=re.IGNORECASE)
        url = re.sub(r'^www\.', '', url, flags=re.IGNORECASE)
        return url.split('/')[0].split('?')[0].split(':')[0].lower()

    def test_dns_udp(self) -> bool:
        try:
            res = subprocess.run(f"nslookup {self.target}", shell=True, capture_output=True, text=True, timeout=4)
            return res.returncode == 0 and ("Address:" in res.stdout or "Name:" in res.stdout)
        except Exception:
            return False

    def test_libc_dns(self) -> bool:
        try:
            res = subprocess.run(f"curl -s -I --max-time 4 https://{self.target}", shell=True, capture_output=True)
            return res.returncode == 0
        except Exception:
            return False

    def resolve_ip(self) -> Optional[str]:
        try:
            return socket.gethostbyname(self.target)
        except Exception:
            return None

    def test_sni_tls(self, ip: str) -> bool:
        try:
            cmd = f"curl -s -I --resolve {self.target}:443:{ip} --max-time 4 https://{self.target}"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return res.returncode == 0 or "HTTP/" in res.stdout
        except Exception:
            return False

    def run(self) -> DiagnosticResult:
        start = time.time()
        udp_ok = self.test_dns_udp()
        libc_ok = self.test_libc_dns()
        ip = self.resolve_ip()
        
        sni_ok = False
        if ip:
            sni_ok = self.test_sni_tls(ip)

        latency = round((time.time() - start) * 1000, 2)
        netd_bug = (udp_ok or sni_ok) and not libc_ok

        return DiagnosticResult(
            target=self.target,
            interface=AndroidAdapter.get_active_interface(),
            dns_udp_ok=udp_ok,
            libc_dns_ok=libc_ok,
            sni_tls_ok=sni_ok,
            resolved_ip=ip,
            netd_bug_detected=netd_bug,
            has_root=AndroidAdapter.has_root(),
            latency_ms=latency
        )
