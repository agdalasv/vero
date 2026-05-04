#!/bin/bash

# Script de prueba para verificar el instalador VERO

echo "🛡️ Probando instalador VERO..."
echo "=================================="

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Crear directorio de prueba
TEST_DIR="/tmp/vero_test"
rm -rf $TEST_DIR
mkdir -p $TEST_DIR

echo "1. Probando estructura de archivos..."
cd /home/agdala/documentos/VERO-Installer

# Verificar archivos requeridos
FILES=("install.sh" "quick_install.sh" "README.md" "LICENSE" ".gitignore")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file existe"
    else
        echo -e "${RED}✗${NC} $file NO existe"
    fi
done

# Verificar directorios
DIRS=("scripts" "config" "docs")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $dir/ existe"
    else
        echo -e "${RED}✗${NC} $dir/ NO existe"
    fi
done

echo ""
echo "2. Verificando scripts..."
SCRIPTS=("scripts/security_ai.py" "scripts/check_traffic.py" "scripts/startup_scan.sh" "scripts/vero")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ] && [ -x "$script" ]; then
        echo -e "${GREEN}✓${NC} $script es ejecutable"
    else
        echo -e "${RED}✗${NC} $script NO es ejecutable o no existe"
    fi
done

echo ""
echo "3. Verificando configuración..."
CONFIGS=("config/threat_db.json" "config/virus_signatures.json")
for config in "${CONFIGS[@]}"; do
    if [ -f "$config" ]; then
        echo -e "${GREEN}✓${NC} $config existe"
    else
        echo -e "${RED}✗${NC} $config NO existe"
    fi
done

echo ""
echo "4. Verificando documentación..."
DOCS=("docs/USER_GUIDE.md" "docs/AI_CONTEXT.md" "README.md" "LICENSE")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}✓${NC} $doc existe"
    else
        echo -e "${RED}✗${NC} $doc NO existe"
    fi
done

echo ""
echo "5. Verificando sintaxis de Python..."
if python3 -m py_compile scripts/security_ai.py 2>/dev/null; then
    echo -e "${GREEN}✓${NC} security_ai.py - Sintaxis correcta"
else
    echo -e "${RED}✗${NC} security_ai.py - Error de sintaxis"
fi

echo ""
echo "=================================="
echo "🛡️ Prueba completada"
echo ""
echo "Para instalar en otra computadora:"
echo "  1. Subir este directorio a GitHub"
echo "  2. En la otra PC: git clone https://github.com/usuario/vero.git"
echo "  3. Ejecutar: cd vero && ./install.sh"
