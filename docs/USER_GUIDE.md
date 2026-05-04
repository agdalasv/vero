# 🛡️ Manual de la Micro IA de Seguridad - VERO

## 🤖 Comando Principal: VERO

**VERO** es el comando principal para interactuar con la micro IA. No necesitas permisos de root.

```bash
vero                           # Estado actual del sistema
vero ayuda                      # Muestra todos los comandos
vero estas en linea              # Verifica si VERO está activo
```

### Escaneo de archivos con VERO
```bash
# Escanear archivos comprimidos
vero revisa este archivo /home/agdala/Descargas/archivo.zip
vero revisa este archivo /home/agdala/Descargas/archivo.rar
vero revisa este archivo /home/agdala/Descargas/archivo.7z
vero revisa este archivo /home/agdala/Descargas/archivo.tar.gz

# Escanear APKs (analiza código interno)
vero revisa este archivo /home/agdala/Descargas/app.apk

# Escanear cualquier archivo
vero revisa este archivo /ruta/al/archivo.exe
```

**Cuando VERO detecta una amenaza:**
1. 🔔 Muestra ventana emergente (notificación)
2. 🗑️ Elimina el archivo automáticamente
3. 📝 Registra la amenaza en los logs

---

## ¿Cómo hacer preguntas a la IA?

Puedes interactuar de dos formas:

### 1. Usando el comando VERO (Recomendado)
```bash
vero reporte                    # Genera reporte completo
vero reporte rapido              # Escaneo rápido
vero actividad sospechosa        # Busca amenazas recientes
vero ips bloqueadas              # Muestra IPs bloqueadas
vero archivos en cuarentena      # Lista archivos en cuarentena
vero logs hoy                    # Muestra logs de hoy
```

### 2. Consultas directas (usando opencode)
Haz preguntas como:
- "Dame el último reporte de seguridad"
- "Qué IPs están bloqueadas actualmente"
- "Analiza el archivo /tmp/.f9ef3fffdbdf87ff-00000000.so"
- "Cuántas amenazas se han detectado hoy"
- "Elimina el archivo sospechoso en /tmp"
- "Muestra los procesos que están corriendo ahora"

### 3. Comandos directos en terminal
```bash
# Reporte completo (escaneo total)
python3 /home/agdala/documentos/security_ai/security_ai.py --report

# Escaneo rápido (solo red y procesos)
python3 /home/agdala/documentos/security_ai/security_ai.py --quick

# Ver el README actual
cat /home/agdala/documentos/README_SECURITY.md

# Ver logs de hoy
cat /home/agdala/documentos/security_ai/logs/security_$(date +%Y%m%d).log

# Ver último reporte JSON
ls -lt /home/agdala/documentos/security_ai/reports/ | head -2
```

### 4. Reportes automáticos
- **Al iniciar la PC:** La IA escanea automáticamente
- **Diario:** 8:00 AM y 8:00 PM se genera reporte automático
- **Manual:** Cuando tú lo solicites

---

## 🔍 Nuevas Capacidades de VERO

### Escaneo de Archivos Comprimidos
VERO ahora puede examinar el **contenido interno** de:
- **ZIP** (.zip)
- **RAR** (.rar, .r00)
- **7-Zip** (.7z)
- **TAR** (.tar, .tar.gz, .tgz, .tar.bz2)

Al detectar amenazas dentro de un archivo comprimido:
1. Extrae temporalmente el contenido
2. Escanea cada archivo interno
3. Si encuentra virus → **Elimina el archivo comprimido completo**
4. Muestra notificación visual

### Análisis de APKs (Android)
VERO puede analizar aplicaciones Android:
- Extrae el contenido de la APK
- Examina archivos `.dex`, `.so`, `.jar`
- Busca código malicioso en la app
- Si detecta amenaza → **Elimina la APK automáticamente**

### Notificaciones Visuales
Cuando detecta una amenaza, VERO muestra:
- **Ventana emergente** (notify-send o zenity)
- **Mensaje:** "¡Archivo Sospechoso! Se detectó: [tipo] en [archivo]"
- **Acción:** El archivo se elimina inmediatamente

---

## 📊 Reportes disponibles

### Reporte principal (README dinámico)
```bash
cat /home/agdala/documentos/README_SECURITY.md
```
Este archivo se actualiza automáticamente cuando:
- Se detecta una amenaza
- Se ejecuta un escaneo
- Hay cambios en el sistema

### Reportes JSON detallados
Ubicación: `/home/agdala/documentos/security_ai/reports/`
```bash
# Ver último reporte
ls -t /home/agdala/documentos/security_ai/reports/ | head -1 | xargs -I {} cat /home/agdala/documentos/security_ai/reports/{}
```

### Logs diarios
Ubicación: `/home/agdala/documentos/security_ai/logs/`
```bash
# Ver log de hoy
cat /home/agdala/documentos/security_ai/logs/security_$(date +%Y%m%d).log
```

---

## 🔍 Qué puede detectar la IA

### Virus y Malware
- TROJAN, WORM, RANSOMWARE, SPYWARE
- ROOTKITS, KEYLOGGERS, BACKDOORS
- CRYPTOMINERS (xmrig, minerd)
- Archivos con firmas sospechosas

### Ataques de Red
- DDoS (muchas conexiones de una IP)
- Fuerza bruta SSH (muchos login fallidos)
- ARP Spoofing
- DNS Poisoning
- Puertos sospechosos abiertos

### Herramientas de Pentesting
- nmap, metasploit, burp, sqlmap
- wireshark, nikto, nessus
- hydra, john, aircrack
- Y más de 20 herramientas

### Spam y Phishing
- Correos sospechosos
- Patrones de phishing
- Intentos de estafa

---

## 🛠️ Acciones que puede hacer la IA

### Automáticas (cuando detecta amenazas)
- ✅ Bloquear IPs maliciosas
- ✅ Terminar procesos virus
- ✅ Poner archivos en cuarentena
- ✅ Activar protección anti-fuerza bruta

### Bajo tu petición
Puedes pedirme:
- "Bloquea la IP 192.168.1.100"
- "Pon en cuarentena el archivo /tmp/sospechoso"
- "Analiza el proceso con PID 1234"
- "Limpia los logs antiguos"
- "Agrega una nueva firma de virus"

---

## 📝 Ejemplos de Uso con VERO

### Consultas rápidas con VERO
```bash
vero                           # Estado actual
vero estas en linea             # Verifica si VERO está activo
vero reporte rapido             # Escaneo rápido
vero ips bloqueadas             # Ver IPs bloqueadas
vero archivos en cuarentena     # Ver archivos en cuarentena
```

### Escaneo de archivos con VERO
```bash
# Archivos comprimidos
vero revisa este archivo /home/agdala/Descargas/archivo.zip
vero revisa este archivo /home/agdala/Descargas/programa.rar
vero revisa este archivo /home/agdala/Descargas/app.7z

# APKs (analiza código interno)
vero revisa este archivo /home/agdala/Descargas/app.apk

# Cualquier archivo
vero revisa este archivo /home/agdala/descargas/programa.exe
```

### Consultas de estado (vía opencode)
- "Cómo está mi PC ahora"
- "Dame un resumen de seguridad"
- "Qué amenazas se han detectado"
- "Mi PC está segura"

### Análisis específicos (vía opencode)
- "Analiza el archivo /home/agdala/descargas/programa.exe"
- "Revisa si hay alguien conectado a mi PC"
- "Checa el tráfico de red actual"
- "Verifica si hay procesos minando cripto"

### Gestión (vía opencode)
- "Desbloquea la IP 1.2.3.4"
- "Restaura el archivo en cuarentena"
- "Limpia todo y haz un escaneo limpio"
- "Desinstala la micro IA"

### Configuración (vía opencode)
- "Que me avise cada hora"
- "Agrega más firmas de virus"
- "No bloquees IPs automáticamente"
- "Cambia la hora de los reportes"

---

## 🚀 Comandos Rápidos con VERO

```bash
# Comandos principales (usar VERO)
vero                           # Estado actual del sistema
vero ayuda                      # Ver todos los comandos
vero reporte                    # Genera reporte completo
vero reporte rapido             # Escaneo rápido
vero estas en linea             # Verifica si VERO está activo
vero actividad sospechosa       # Busca amenazas recientes
vero ips bloqueadas             # Muestra IPs bloqueadas
vero archivos en cuarentena     # Lista archivos en cuarentena
vero logs hoy                   # Muestra logs de hoy

# Escanear archivos (muy fácil)
vero revisa este archivo /home/agdala/Descargas/archivo.zip
vero revisa este archivo /home/agdala/Descargas/app.apk
vero revisa este archivo /ruta/al/archivo.exe

# Comandos avanzados (solo si necesitas)
python3 /home/agdala/documentos/security_ai/security_ai.py --report
python3 /home/agdala/documentos/security_ai/security_ai.py --quick
cat /home/agdala/documentos/README_SECURITY.md
cat /home/agdala/documentos/security_ai/state.json
ls /home/agdala/documentos/security_ai/quarantine/
```

---

## 📞 Soporte y Ayuda

### Usando VERO (Recomendado)
```bash
vero ayuda     # Muestra todos los comandos disponibles
vero           # Estado actual del sistema
```

### Usando opencode
Para cualquier duda, pregunta o mejora:
1. Haz tu pregunta directamente a **opencode**
2. Menciona "VERO", "micro IA" o "seguridad"
3. Especifica qué quieres saber o hacer

La IA está siempre monitoreando y aprendiendo de nuevas amenazas.

---

## ⚡ Resumen Rápido

| Acción | Comando |
|--------|---------|
| Estado actual | `vero` |
| Ayuda | `vero ayuda` |
| Escanear archivo | `vero revisa este archivo /ruta/al/archivo` |
| Escanear APK | `vero revisa este archivo /ruta/app.apk` |
| Escanear ZIP/RAR | `vero revisa este archivo /ruta/archivo.zip` |
| Ver IPs bloqueadas | `vero ips bloqueadas` |
| Ver cuarentena | `vero archivos en cuarentena` |
| Reporte completo | `vero reporte` |
| Verificar si está activo | `vero estas en linea` |

---

*Última actualización: 2026-05-03*
*Peso del sistema: 104KB*
*Estado: ACTIVO Y PROTEGIENDO* 🛡️
*Nombre de la IA: **VERO***
