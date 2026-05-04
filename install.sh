#!/bin/bash

# VERO - Micro IA de Seguridad (Instalador)
# Instala todo el sistema de seguridad en una nueva computadora

set -e

echo "=========================================="
echo "  VERO - Instalador de Micro IA"
echo "  Seguridad Local Proactiva"
echo "=========================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar si se ejecuta como root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}⚠️  Advertencia: No es necesario ejecutar como root${NC}"
    echo -e "${YELLOW}   El instalador usará sudo cuando sea necesario${NC}"
    echo ""
fi

# 1. Instalar dependencias
echo -e "${GREEN}[1/7] Instalando dependencias...${NC}"
sudo apt-get update
sudo apt-get install -y python3 python3-psutil p7zip-full unzip rar unrar notify-osd zenity

# 2. Crear directorios
echo -e "${GREEN}[2/7] Creando estructura de directorios...${NC}"
mkdir -p /home/$USER/documentos/security_ai/{logs,reports,quarantine}
mkdir -p /usr/local/bin

# 3. Copiar scripts principales
echo -e "${GREEN}[3/7] Instalando scripts principales...${NC}"
cp scripts/security_ai.py /home/$USER/documentos/security_ai/
cp scripts/check_traffic.py /home/$USER/documentos/security_ai/
cp scripts/startup_scan.sh /home/$USER/documentos/security_ai/
chmod +x /home/$USER/documentos/security_ai/*.py
chmod +x /home/$USER/documentos/security_ai/*.sh

# 4. Copiar configuración
echo -e "${GREEN}[4/7] Instalando configuración...${NC}"
cp config/threat_db.json /home/$USER/documentos/security_ai/
cp config/virus_signatures.json /home/$USER/documentos/security_ai/
touch /home/$USER/documentos/security_ai/state.json
echo '{"blocked_ips": [], "quarantined_files": []}' > /home/$USER/documentos/security_ai/state.json
touch /home/$USER/documentos/security_ai/integrity_db.json
echo '{}' > /home/$USER/documentos/security_ai/integrity_db.json

# 5. Instalar comando VERO
echo -e "${GREEN}[5/7] Instalando comando VERO...${NC}"
sudo cp scripts/vero /usr/local/bin/
sudo chmod +x /usr/local/bin/vero

# 6. Configurar servicio systemd
echo -e "${GREEN}[6/7] Configurando servicio systemd...${NC}"
sudo tee /etc/systemd/system/vero_security.service > /dev/null << 'EOF'
[Unit]
Description=VERO Security AI Startup Scan
After=network.target

[Service]
Type=oneshot
User=%i
ExecStart=/home/%i/documentos/security_ai/startup_scan.sh
RemainAfterExit=no

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable vero_security.service

# 7. Configurar cron jobs
echo -e "${GREEN}[7/7] Configurando reportes automáticos...${NC}"
(crontab -l 2>/dev/null | grep -v "security_ai"; echo "0 8,20 * * * python3 /home/$USER/documentos/security_ai/security_ai.py --report") | crontab -

# Copiar documentación
echo -e "${GREEN}Copiando documentación...${NC}"
cp docs/USER_GUIDE.md /home/$USER/documentos/security_ai/
cp docs/AI_CONTEXT.md /home/$USER/documentos/security_ai/
touch /home/$USER/documentos/README_SECURITY.md

# Establecer permisos
chown -R $USER:$USER /home/$USER/documentos/security_ai/

echo ""
echo -e "${GREEN}=========================================="
echo -e "  ¡VERO instalado exitosamente! 🛡️"
echo -e "==========================================${NC}"
echo ""
echo "Comandos disponibles:"
echo "  vero                    - Ver estado de seguridad"
echo "  vero estas en linea     - Verificar si VERO está activo"
echo "  vero reporte            - Generar reporte completo"
echo "  vero revisa este archivo [ruta] - Escanear archivo"
echo ""
echo "Documentación:"
echo "  vero ayuda              - Ver todos los comandos"
echo "  cat /home/$USER/documentos/security_ai/USER_GUIDE.md"
echo ""
echo "Servicios activos:"
echo "  - Servicio systemd: vero_security.service"
echo "  - Cron jobs: Reportes 8am y 8pm"
echo ""
echo "¡Tu PC está protegida! 🛡️"
