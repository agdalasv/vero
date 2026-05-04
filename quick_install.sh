#!/bin/bash

# VERO - Instalación Rápida (Un solo comando)
# Uso: curl -sSL https://raw.githubusercontent.com/usuario/vero/main/quick_install.sh | bash

set -e

echo "🛡️ VERO - Instalación Rápida"
echo "=================================="

# 1. Descargar repositorio
if command -v git >/dev/null 2>&1; then
    echo "[1/3] Clonando repositorio..."
    git clone https://github.com/usuario/vero.git /tmp/vero_install
else
    echo "[1/3] Git no encontrado, descargando con wget..."
    wget -q https://github.com/usuario/vero/archive/main.zip -O /tmp/vero.zip
    apt-get install -y unzip >/dev/null 2>&1
    unzip -q /tmp/vero.zip -d /tmp/
    mv /tmp/vero-main /tmp/vero_install
fi

# 2. Ejecutar instalador
echo "[2/3] Ejecutando instalador..."
cd /tmp/vero_install
chmod +x install.sh
./install.sh

# 3. Limpiar
echo "[3/3] Limpiando archivos temporales..."
rm -rf /tmp/vero_install /tmp/vero.zip

echo ""
echo "✅ ¡VERO instalado exitosamente!"
echo "Usa 'vero' para comenzar"
