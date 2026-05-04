# 🛡️ VERO - Micro IA de Seguridad Personal

**Sistema de defensa local proactiva contra virus, ataques, spam y amenazas en archivos comprimidos/APKs.**

### 🐧 Compatible con Linux
- Ubuntu, Debian, Linux Mint, Fedora, CentOS, Arch Linux
- Requiere: Python 3.8+, systemd, iptables
- Arquitectura: x86_64 (64-bit)

[![GitHub](https://img.shields.io/badge/GitHub-VERO-black?style=flat&logo=github)](https://github.com/agdalasv/vero)
[![Website](https://img.shields.io/badge/Web-vero.netlify.app-blue?style=flat&logo=github-pages)](https://agdalasv.github.io/vero/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## 🌐 Página Web

Visita la página oficial de VERO:
**https://agdalasv.github.io/vero/**

---

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/agdalasv/vero.git
cd vero

# Ejecutar instalador
chmod +x install.sh
./install.sh
```

---

## ✨ Características Principales

### 🤖 Comando Principal: `vero`
```bash
vero                           # Saludo y estado breve
vero ayuda                      # Ver todos los comandos
vero estas en linea             # Verificar si VERO está activo
vero reporte                    # Generar reporte completo
vero revisa este archivo [ruta] # Escanear archivo específico
```

### 🔍 Detección Completa
- **Virus/Malware:** Trojan, Worm, Ransomware, Spyware, Rootkit, Keylogger, Cryptominers
- **Ataques de Red:** DDoS, Fuerza bruta SSH, ARP Spoofing, DNS Poisoning
- **Herramientas de Pentesting:** 25+ herramientas (nmap, metasploit, sqlmap, burp, etc.)
- **Spam/Phishing:** Patrones en correos y archivos
- **Archivos Comprimidos:** ZIP, RAR, 7Z, TAR, TAR.GZ - Escanea contenido interno
- **APKs Android:** Analiza código interno (.dex, .so, .jar)

### 🛡️ Protección Automática
- ✅ Bloqueo de IPs maliciosas
- ✅ Terminación de procesos virus
- ✅ Cuarentena de archivos sospechosos
- ✅ Eliminación automática de amenazas en descargas
- ✅ Notificaciones visuales al detectar amenazas

---

## 📦 Estructura del Proyecto

```
VERO-Installer/
├── install.sh              # Script de instalación automática
├── README.md              # Este archivo
├── LICENSE                # Licencia MIT
├── scripts/
│   ├── security_ai.py    # Núcleo principal (34KB)
│   ├── check_traffic.py  # Monitoreo de red (1.1KB)
│   ├── startup_scan.sh   # Script de inicio
│   └── vero             # Comando principal (7.9KB)
├── config/
│   ├── threat_db.json    # Base de datos de amenazas
│   └── virus_signatures.json # Firmas de virus
└── docs/
    ├── USER_GUIDE.md     # Manual para el usuario
    └── AI_CONTEXT.md     # Documentación técnica
```

---

## 🎯 Uso Básico

### Ver estado de seguridad
```bash
vero
# Salida:
# ¡Hola! Soy VERO, tu Micro IA de Seguridad 🛡️
# ## Estado del Sistema: ✅ SECURE
# - **Hostname:** mi-pc
# - **Amenazas detectadas:** 0
# ...
```

### Escanear archivos
```bash
# Archivos comprimidos
vero revisa este archivo ~/Descargas/archivo.zip
vero revisa este archivo ~/Descargas/programa.rar

# APKs (analiza código interno)
vero revisa este archivo ~/Descargas/app.apk

# Cualquier archivo
vero revisa este archivo ~/Descargas/programa.exe
```

**Al detectar amenazas:**
1. 🔔 Muestra ventana emergente (notificación)
2. 🗑️ Elimina el archivo automáticamente
3. 📝 Registra la amenaza en los logs

---

## 🔧 Configuración Automática

El instalador configura automáticamente:
- ✅ **Servicio systemd:** Escaneo al iniciar la PC
- ✅ **Cron jobs:** Reportes diarios (8:00 AM y 8:00 PM)
- ✅ **Comando `vero`:** Disponible globalmente sin necesidad de root
- ✅ **Dependencias:** python3-psutil, p7zip-full, unzip, rar, unrar, notify-osd, zenity

---

## 📊 Reportes

### Reporte dinámico
```bash
cat ~/documentos/README_SECURITY.md
```
Se actualiza automáticamente cuando:
- Se detecta una amenaza
- Se ejecuta un escaneo
- Hay cambios en el sistema

### Logs diarios
```bash
cat ~/documentos/security_ai/logs/security_$(date +%Y%m%d).log
```

### Reportes JSON detallados
```bash
ls -lt ~/documentos/security_ai/reports/ | head -2
```

---

## 🛠️ Actualización de Firmas

### Agregar nuevas firmas de virus
```bash
nano ~/documentos/security_ai/virus_signatures.json
```

### Agregar nuevas herramientas de pentesting
```bash
nano ~/documentos/security_ai/threat_db.json
```

### Probar cambios
```bash
vero reporte rapido
```

---

## 📝 Documentación

- **Manual del usuario:** `vero ayuda` o `cat ~/documentos/security_ai/USER_GUIDE.md`
- **Documentación técnica:** `cat ~/documentos/security_ai/AI_CONTEXT.md`
- **Reporte actual:** `cat ~/documentos/README_SECURITY.md`

---

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama de características (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📞 Soporte

- **Reportar problemas:** [GitHub Issues](https://github.com/agdalasv/vero/issues)
- **Preguntas:** Usa `vero ayuda` o consulta la documentación

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 🙏 Agradecimientos

- **Desarrollado por:** Agdala - 2026
- **Inspirado en:** Necesidad de seguridad local proactiva
- **Peso total:** ~104KB (ultra liviano)

---

## ☕ Invita un Café

Si te gusta VERO y quieres apoyar el desarrollo, puedes hacer una donación:

**Wallet BTC:** `3L8f3v6BWwL7KBcb8AMZQ2bpE3ACne2EUf`

¡Gracias por tu apoyo! 🎉

---

## 🐛 Reportar Bugs

¿Encontraste un bug? Escríbenos:

**Email:** agdala.sv@gmail.com

O abre un issue en GitHub:
https://github.com/agdalasv/vero/issues

---

## 📜 Licencia

**MIT License - 2026 Agdala**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

---

*Última actualización: 2026-05-03*
*Versión: 1.0 - VERO*
*Desarrollado por: Agdala 2026*
*Estado: ACTIVO Y PROTEGIENDO* 🛡️
