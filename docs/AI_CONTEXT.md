# 🤖 Contexto Técnico - Micro IA de Seguridad - VERO

*Archivo de referencia para el asistente AI - Última actualización: 2026-05-03 21:30*

## 📋 Resumen General
- **Nombre de la IA:** VERO
- **Propósito:** Defensa local proactiva contra amenazas, virus, ataques y spam
- **Peso total:** 104KB (incluye logs y reportes generados)
- **Estado:** ACTIVO (servicio systemd + cron jobs)
- **Ubicación base:** `/home/agdala/documentos/security_ai/`
- **Comando principal:** `vero` (ubicado en `/usr/local/bin/vero`)
- **Reporte dinámico:** `/home/agdala/documentos/README_SECURITY.md`

## 🛠️ Historia de Creación (Pasos Ejecutados)
1. Creación de directorios base: `mkdir -p /home/agdala/documentos/security_ai/{logs,reports,quarantine}`
2. Instalación de dependencia: `apt-get install python3-psutil`
3. Creación de `security_ai.py` (núcleo de 27KB con detección completa)
4. Creación de `check_traffic.py` (monitoreo de red de 1.1KB)
5. Creación de `startup_scan.sh` (script de inicio)
6. Configuración de servicio systemd: `/etc/systemd/system/security_ai_service.service`
7. Activación de servicio: `systemctl enable security_ai_service.service`
8. Configuración de cron jobs: Reportes diarios 8am y 8pm
9. Corrección de errores: JSON serialization, falsos positivos en detección de procesos
10. Actualización de firmas de virus y reglas YARA-like
11. **NUEVO:** Instalación de herramientas para archivos comprimidos: `apt-get install p7zip-full unzip rar unrar notify-osd zenity`
12. **NUEVO:** Agregada función `scan_compressed_file()` para ZIP, RAR, 7Z, TAR, etc.
13. **NUEVO:** Agregada función `scan_apk_file()` para análisis de código interno de APKs
14. **NUEVO:** Agregada función `monitor_downloads()` para monitoreo de descargas
15. **NUEVO:** Agregada función `show_notification()` para ventanas emergentes
16. **NUEVO:** Creación del comando `vero` en `/usr/local/bin/vero` (5.8KB)
17. **NUEVO:** Actualización de `USER_GUIDE.md` con instrucciones de VERO
18. **NUEVO:** VERO saluda con "¡Hola! Soy VERO..." al ejecutar `vero` sin parámetros
19. **NUEVO:** Corrección para mostrar estado breve (no reporte completo) al usar `vero`

## 📁 Estructura de Archivos
```
/home/agdala/documentos/security_ai/
├── security_ai.py          (27KB) - Núcleo principal de la IA
├── check_traffic.py        (1.1KB) - Monitoreo de tráfico de red
├── startup_scan.sh         (263B) - Script de escaneo al inicio
├── threat_db.json          (1.7KB) - Base de datos de amenazas conocidas
├── virus_signatures.json   (550B) - Firmas de virus y patrones
├── integrity_db.json       (371B) - Hashes de integridad de archivos críticos
├── state.json              (102B) - Estado actual (IPs bloqueadas, cuarentena)
├── logs/                   - Logs diarios de seguridad
├── reports/                - Reportes JSON detallados
├── quarantine/              - Archivos en cuarentena
├── USER_GUIDE.md           (8KB) - Manual para el usuario (actualizado con VERO)
├── AI_CONTEXT.md           (12KB) - Este archivo de referencia
└── /usr/local/bin/vero    (5.8KB) - Comando principal para interactuar con VERO

/home/agdala/documentos/
├── README_SECURITY.md      - Reporte dinámico (se actualiza automáticamente)
└── (otros documentos del usuario)
```

## ⚙️ Procesos Clave
### 1. Comando VERO (Principal)
- **Ubicación:** `/usr/local/bin/vero` (5.8KB)
- **Permisos:** Ejecutable sin necesidad de root
- **Funcionalidad:**
  - `vero` → Saluda y muestra estado breve
  - `vero ayuda` → Muestra todos los comandos
  - `vero reporte` → Genera reporte completo
  - `vero estas en linea` → Verifica si VERO está activo
  - `vero revisa este archivo [ruta]` → Escanea archivo específico

### 2. Escaneo al Inicio (Systemd)
- **Servicio:** `security_ai_service.service`
- **Ejecución:** Al iniciar la PC
- **Script:** `/home/agdala/documentos/security_ai/startup_scan.sh`
- **Salida:** `/home/agdala/documentos/security_ai/startup.log`

### 3. Reportes Diarios (Cron)
- **Horarios:** 8:00 AM y 8:00 PM
- **Comando:** `python3 /home/agdala/documentos/security_ai/security_ai.py --report`
- **Resultado:** Actualiza README y genera reporte JSON

### 4. Modos de Ejecución
```bash
# Escaneo completo (red, procesos, archivos, integridad)
python3 /home/agdala/documentos/security_ai/security_ai.py --report

# Escaneo rápido (solo red y procesos)
python3 /home/agdala/documentos/security_ai/security_ai.py --quick

# Modo daemon (ejecución continua cada hora)
python3 /home/agdala/documentos/security_ai/security_ai.py --daemon

# Usar VERO (recomendado)
vero
vero revisa este archivo /ruta/al/archivo.zip
```

## 🔍 Capacidades de Detección
### Amenazas Soportadas
- **Virus/Malware:** Trojan, Worm, Ransomware, Spyware, Rootkit, Keylogger, Cryptominer
- **Ataques de Red:** DDoS, Fuerza bruta SSH, ARP Spoofing, DNS Poisoning
- **Herramientas de Pentesting:** 25+ herramientas (nmap, metasploit, sqlmap, burp, etc.)
- **Spam/Phishing:** Patrones en correos y archivos
- **Archivos Sospechosos:** En /tmp, /dev/shm, rutas críticas del sistema
- **NUEVO:** Archivos comprimidos (ZIP, RAR, 7Z, TAR, TAR.GZ, TGZ, TAR.BZ2)
- **NUEVO:** APKs Android (análisis de código interno .dex, .so, .jar)

### Bases de Datos
1. `threat_db.json`:
   - `pentesting_tools`: Lista de herramientas de pentesting a detectar
   - `virus_names`: Nombres de malware a buscar en procesos
   - `suspicious_ports`: Puertos que indican actividad sospechosa
   - `spam_indicators`: Palabras clave de spam

2. `virus_signatures.json`:
   - `md5`: Firmas MD5 de virus conocidos (EICAR test, mineros)
   - `patterns`: Expresiones regulares para detectar shellcode
   - `yara_like`: Reglas para detectar backdoors, downloaders, keyloggers

### NUEVAS Funciones en `security_ai.py`
1. **`scan_compressed_file(filepath)`**:
   - Extrae archivos comprimidos (ZIP, RAR, 7Z, TAR, etc.) a directorio temporal
   - Escanea cada archivo interno con `scan_file_for_viruses()`
   - Reporta el archivo comprimido que contenía la amenaza
   - Requiere: `p7zip-full`, `unzip`, `rar`, `unrar`

2. **`scan_apk_file(filepath)`**:
   - Extrae el contenido de la APK
   - Examina archivos `.dex`, `.so`, `.jar`
   - Busca código malicioso usando firmas y patrones
   - Requiere: `p7zip-full`

3. **`monitor_downloads()`**:
   - Monitorea directorios de descargas (`/home/agdala/Descargas`, `Downloads`, `/tmp`)
   - Detecta amenazas en archivos nuevos
   - **Elimina automáticamente** archivos sospechosos
   - Se integra en `run_scan()`

4. **`show_notification(title, message, urgency)`**:
   - Muestra ventana emergente con `notify-send` o `zenity`
   - Avisa al instante de amenazas detectadas
   - Mensaje indica qué archivo se eliminó
   - Requiere: `notify-osd`, `zenity`

## 🔄 Proceso de Actualizaciones
### 1. Actualizar Firmas de Virus
```bash
# Editar archivo de firmas
nano /home/agdala/documentos/security_ai/virus_signatures.json
# Agregar nuevos hashes MD5, patrones o reglas YARA-like
```

### 2. Agregar Nuevas Amenazas
```bash
# Editar base de datos de amenazas
nano /home/agdala/documentos/security_ai/threat_db.json
# Agregar nuevas herramientas de pentesting, nombres de virus, puertos
```

### 3. Actualizar Lógica de la IA
```bash
# Editar núcleo de la IA
nano /home/agdala/documentos/security_ai/security_ai.py
# Probar cambios con: python3 security_ai.py --quick
```

### 4. Actualizar Cron Jobs
```bash
crontab -e
# Modificar horarios de reportes diarios
```

### 5. Actualizar Servicio Systemd
```bash
sudo nano /etc/systemd/system/security_ai_service.service
sudo systemctl daemon-reload
sudo systemctl restart security_ai_service.service
```

## 🛡️ Mecanismos de Protección Automática
1. **Bloqueo de IPs:** `iptables -A INPUT -s IP -j DROP`
2. **Terminación de Procesos:** `os.kill(pid, signal.SIGKILL)`
3. **Cuarentena de Archivos:** Movimiento a `/home/agdala/documentos/security_ai/quarantine/`
4. **Protección Anti-Fuerza Bruta:** Reglas de iptables para limitar intentos SSH
5. **NUEVO:** **Eliminación Automática:** Archivos sospechosos en descargas se eliminan (`os.remove()`)
6. **NUEVO:** **Notificacón Visual:** Ventanas emergentes al detectar amenazas (`notify-send`/`zenity`)

## 📊 Estado Actual del Sistema
- **Comando VERO:** Ubicado en `/usr/local/bin/vero` (5.8KB)
- **IPs bloqueadas:** 0 (al 2026-05-03 21:20)
- **Archivos en cuarentena:** 2 (falsos positivos corregidos)
- **Amenazas detectadas hoy:** 2 (nivel medio)
- **Servicios activos:** systemd + cron + vero command
- **Capacidades nuevas:** Escaneo de archivos comprimidos, APKs, notificaciones visuales

## 📊 Estado Actual del Sistema
- **IPs bloqueadas:** 0 (al 2026-05-03 21:20)
- **Archivos en cuarentena:** 2 (falsos positivos corregidos)
- **Amenazas detectadas hoy:** 2 (nivel medio)
- **Servicios activos:** systemd + cron + comando vero
- **NUEVO:** Capacidad de escanear archivos comprimidos y APKs
- **NUEVO:** Notificaciones visuales con eliminación automática

## 🔧 Troubleshooting Común
### Error de JSON Serialization
- Causa: Bytes en virus_signatures.json
- Solución: Asegurar que todos los patrones sean strings, no bytes

### Falsos Positivos
- Causa: Coincidencias parciales en nombres de procesos
- Solución: Usar `re.search(r'\b' + re.escape(term) + r'\b', string)`

### Servicio no inicia
```bash
sudo systemctl status security_ai_service.service
journalctl -u security_ai_service.service
```

### Comando VERO no funciona
```bash
# Verificar si existe
ls -lh /usr/local/bin/vero

# Verificar permisos
chmod +x /usr/local/bin/vero

# Verificar sintaxis Python
python3 -m py_compile /usr/local/bin/vero
```

### Error al escanear archivos comprimidos
```bash
# Verificar herramientas instaladas
which 7z unzip unrar

# Instalar si falta
apt-get install p7zip-full unzip rar unrar
```

### Notificaciones no aparecen
```bash
# Verificar herramientas de notificación
which notify-send zenity

# Instalar si falta
apt-get install notify-osd zenity
```

## 📞 Comandos de Consulta Rápida
### Con VERO (Recomendado)
```bash
vero                           # Estado actual (saluda y muestra resumen)
vero ayuda                      # Ver todos los comandos
vero estas en linea             # Verifica si VERO está activo
vero reporte                    # Genera reporte completo
vero reporte rapido             # Escaneo rápido
vero ips bloqueadas             # Muestra IPs bloqueadas
vero archivos en cuarentena     # Lista archivos en cuarentena
vero revisa este archivo [ruta] # Escanea archivo específico
vero logs hoy                   # Muestra logs de hoy
```

### Comandos del Sistema
```bash
# Ver estado del servicio
systemctl status security_ai_service.service

# Ver cron jobs activos
crontab -l | grep security

# Ver último reporte
cat /home/agdala/documentos/README_SECURITY.md

# Ver estado de IPs bloqueadas
cat /home/agdala/documentos/security_ai/state.json

# Ver logs de hoy
cat /home/agdala/documentos/security_ai/logs/security_$(date +%Y%m%d).log

# Ver archivo de contexto
cat /home/agdala/documentos/security_ai/AI_CONTEXT.md
```

## 📝 Notas para el Asistente
- Al recibir preguntas sobre VERO o la micro IA, consultar este archivo primero
- **VERO** es el nombre de la IA y el comando principal (`/usr/local/bin/vero`)
- Para actualizar la IA, seguir los pasos en "Proceso de Actualizaciones"
- Siempre probar cambios con `--quick` antes de aplicar en producción
- El reporte dinámico (README_SECURITY.md) se actualiza automáticamente
- Los archivos en cuarentena se guardan en `/home/agdala/documentos/security_ai/quarantine/`
- VERO puede escanear archivos comprimidos y APKs analizando su contenido interno
- Notificaciones visuales se muestran automáticamente al detectar amenazas
- Comandos de VERO no requieren permisos de root

## 🔄 Actualizaciones Recientes (2026-05-03 21:30)
1. **Comando VERO:** Creado `/usr/local/bin/vero` para interactuar sin root
2. **Escaneo de Archivos Comprimidos:** ZIP, RAR, 7Z, TAR, etc.
3. **Análisis de APKs:** Escanea código interno (.dex, .so, .jar)
4. **Notificaciones Visuales:** Ventanas emergentes con notify-send/zenity
5. **Eliminación Automática:** Archivos sospechosos se eliminan al detectarse
6. **Saludo Personalizado:** `vero` saluda con "¡Hola! Soy VERO..."
7. **Manual Actualizado:** `USER_GUIDE.md` con instrucciones de VERO
8. **Contexto Actualizado:** `AI_CONTEXT.md` con toda la info nueva

---
*Este archivo permite al asistente recordar toda la configuración y procesos de la micro IA sin necesidad de re-derivar información.*
*Nombre de la IA: **VERO***
*Última actualización: 2026-05-03 21:30*
