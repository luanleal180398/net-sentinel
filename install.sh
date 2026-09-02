#!/bin/bash
set -e

echo -e "\033[96m[*] Instalando dependências necessárias no Termux...\033[0m"
pkg update -y && pkg install python curl dnsutils git -y > /dev/null 2>&1

INSTALL_DIR="$HOME/net-sentinel"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "\033[93m[*] Atualizando repositório existente...\033[0m"
    cd "$INSTALL_DIR" && git pull origin main 2>/dev/null || true
else
    echo -e "\033[96m[*] Baixando o NetSentinel do GitHub...\033[0m"
    git clone https://github.com/SEU_USUARIO/net-sentinel.git "$INSTALL_DIR"
fi

echo -e "\033[96m[*] Vinculando o executável ao sistema...\033[0m"
echo '#!/usr/bin/env python3' > $PREFIX/bin/net-sentinel
echo 'import sys' >> $PREFIX/bin/net-sentinel
echo "sys.path.insert(0, '$INSTALL_DIR')" >> $PREFIX/bin/net-sentinel
echo 'from net_sentinel.cli import main' >> $PREFIX/bin/net-sentinel
echo 'if __name__ == "__main__": main()' >> $PREFIX/bin/net-sentinel

chmod +x $PREFIX/bin/net-sentinel

echo -e "\033[92m[✓] NetSentinel instalado com sucesso!\033[0m"
echo -e "\033[93mAgora você pode usar digitando:\033[0m net-sentinel google.com"
