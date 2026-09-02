import subprocess
import time
import re

class AndroidAdapter:
    @staticmethod
    def get_active_interface() -> str:
        try:
            res = subprocess.run("ip route get 1.1.1.1", shell=True, capture_output=True, text=True, timeout=3)
            match = re.search(r'dev\s+(\S+)', res.stdout)
            return match.group(1) if match else "desconhecida"
        except Exception:
            return "desconhecida"

    @staticmethod
    def has_root() -> bool:
        return subprocess.run("which su", shell=True, capture_output=True).returncode == 0

    @staticmethod
    def toggle_airplane_mode():
        subprocess.run("cmd connectivity airplane-mode enable 2>/dev/null", shell=True)
        time.sleep(1.5)
        subprocess.run("cmd connectivity airplane-mode disable 2>/dev/null", shell=True)

    @staticmethod
    def force_root_netd_flush():
        cmds = [
            "su -c 'ndc resolver flushdefaultif'",
            "su -c 'settings put global private_dns_mode hostname'",
            "su -c 'settings put global private_dns_specifier dns.google'"
        ]
        for cmd in cmds:
            subprocess.run(cmd, shell=True, capture_output=True)
