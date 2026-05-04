#!/usr/bin/env python3
import os
import json
import subprocess
import socket
import psutil
import datetime
import hashlib
import signal
import sys
import re
import time
import tempfile
import shutil
from pathlib import Path
from collections import defaultdict, Counter

class SecurityAI:
    def __init__(self):
        self.base_path = Path("/home/agdala/documentos/security_ai")
        self.log_path = self.base_path / "logs"
        self.report_path = self.base_path / "reports"
        self.threat_db = self.base_path / "threat_db.json"
        self.state_file = self.base_path / "state.json"
        self.virus_sigs = self.base_path / "virus_signatures.json"
        self.readme_path = Path("/home/agdala/documentos/README_SECURITY.md")
        
        self.threats_found = []
        self.network_connections = []
        self.suspicious_ips = set()
        self.blocked_ips = set()
        self.quarantined_files = []
        
        self.load_state()
        self.load_threat_db()
        self.load_virus_signatures()
        
    def load_state(self):
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    state = json.load(f)
                    self.blocked_ips = set(state.get('blocked_ips', []))
                    self.quarantined_files = state.get('quarantined_files', [])
            except:
                pass
    
    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump({
                'blocked_ips': list(self.blocked_ips),
                'quarantined_files': self.quarantined_files
            }, f)
    
    def load_threat_db(self):
        if self.threat_db.exists():
            with open(self.threat_db) as f:
                self.known_threats = json.load(f)
        else:
            self.known_threats = {
                "suspicious_ports": [21, 22, 23, 445, 3389, 5900, 8080, 4444, 31337],
                "pentesting_tools": [
                    "nmap", "metasploit", "msfconsole", "aircrack", "john", "hydra",
                    "wireshark", "tcpdump", "netcat", "nc", "ncat", "nikto", "burp",
                    "sqlmap", "nessus", "openvas", "acunetix", "w3af", "beef",
                    "setoolkit", "social-engineer-toolkit", "maltego", "recon-ng",
                    "theharvester", "fierce", "dnsenum", "dirb", "gobuster", "ffuf",
                    "masscan", "zmap", "hping3", "slowloris", "goldeneye", "torshammer"
                ],
                "virus_names": [
                    "trojan", "worm", "ransomware", "spyware", "adware", "rootkit",
                    "keylogger", "botnet", "cryptominer", "minerd", "xmrig", "backdoor",
                    "rat", "remote access trojan", "infostealer", "credential stealer",
                    "loader", "dropper", "exploit", "shellcode", "payload", "meterpreter"
                ],
                "spam_indicators": [
                    "mailbomb", "spam", "phishing", "scam", "fake", "lottery",
                    "inheritance", "prince", "nigeria", "bitcoin", "crypto giveaway"
                ],
                "attack_patterns": [
                    "sql injection", "xss", "csrf", "lfi", "rfi", "directory traversal",
                    "buffer overflow", "heap spray", "use after free", "race condition"
                ],
                "suspicious_paths": [
                    "/tmp", "/dev/shm", "/var/tmp", "/proc/self", "/root/.ssh",
                    "/home/*/.ssh", "/etc/cron*", "/var/spool/cron"
                ],
                "bad_hashes": []
            }
            self.save_threat_db()
    
    def save_threat_db(self):
        with open(self.threat_db, 'w') as f:
            json.dump(self.known_threats, f, indent=2)
    
    def load_virus_signatures(self):
        if self.virus_sigs.exists():
            with open(self.virus_sigs) as f:
                self.virus_signatures = json.load(f)
        else:
            self.virus_signatures = {
                "md5": {
                    "eicar_test": "44d88612fea8a8f36de82e1278abb02f",
                    "common_miner": "c6ca2e75d9eb6f1d2c5dd4e7e5f5e5e5"
                },
                "patterns": [
                    "\\x90\\x90\\x90\\x90",
                    "cmd\\.exe.*/c",
                    "powershell.*-enc",
                    "wget.*http.*\\|.*sh",
                    "curl.*\\|.*bash"
                ],
                "yara_like": [
                    {"name": "possible_backdoor", "pattern": "exec\\s*\\("},
                    {"name": "possible_downloader", "pattern": "urllib.*urlopen"},
                    {"name": "possible_keylogger", "pattern": "pynput|keyboard\\.on_press"}
                ]
            }
            with open(self.virus_sigs, 'w') as f:
                json.dump(self.virus_signatures, f, indent=2)
    
    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        log_file = self.log_path / f"security_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a') as f:
            f.write(log_entry + "\n")
    
    def calculate_hash(self, filepath):
        try:
            hasher = hashlib.md5()
            with open(filepath, 'rb') as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except:
            return None
    
    def scan_file_for_viruses(self, filepath):
        try:
            if not os.path.isfile(filepath):
                return None
            
            if filepath.endswith('.bash_history') or filepath.endswith('.history'):
                return None
            
            file_hash = self.calculate_hash(filepath)
            if file_hash and file_hash in self.virus_signatures.get("md5", {}):
                return {
                    'type': 'virus_md5_match',
                    'file': filepath,
                    'hash': file_hash,
                    'severity': 'critical'
                }
            
            with open(filepath, 'rb') as f:
                content = f.read(10240)
            
            for sig_name, sig_hash in self.virus_signatures.get("md5", {}).items():
                if file_hash == sig_hash:
                    return {
                        'type': 'virus_known',
                        'file': filepath,
                        'virus_name': sig_name,
                        'severity': 'critical'
                    }
            
            for pattern in self.virus_signatures.get("patterns", []):
                try:
                    if re.search(pattern, content.decode('utf-8', errors='ignore')):
                        return {
                            'type': 'virus_pattern_match',
                            'file': filepath,
                            'pattern': str(pattern),
                            'severity': 'high'
                        }
                except:
                    pass
            
            content_str = content.decode('utf-8', errors='ignore')
            for sig in self.virus_signatures.get("yara_like", []):
                try:
                    if re.search(sig["pattern"], content_str):
                        return {
                            'type': 'virus_yara_match',
                            'file': filepath,
                            'rule': sig["name"],
                            'severity': 'high'
                        }
                except:
                    pass
            
            return None
        except:
            return None
    
    def show_notification(self, title, message, urgency="critical"):
        try:
            subprocess.run([
                'notify-send', '-u', urgency, title, message
            ], timeout=5)
        except:
            try:
                subprocess.run([
                    'zenity', '--warning', '--title', title, '--text', message
                ], timeout=5)
            except:
                pass
    
    def scan_compressed_file(self, filepath):
        threats = []
        temp_dir = None
        
        try:
            temp_dir = tempfile.mkdtemp(prefix="security_ai_scan_")
            self.log(f"Escaneando archivo comprimido: {filepath}")
            
            if filepath.endswith('.zip'):
                subprocess.run(['unzip', '-q', filepath, '-d', temp_dir], timeout=30)
            elif filepath.endswith(('.rar', '.r00')):
                subprocess.run(['unrar', 'x', filepath, temp_dir + '/'], timeout=30)
            elif filepath.endswith(('.7z', '.7zip')):
                subprocess.run(['7z', 'x', filepath, f'-o{temp_dir}', '-y'], timeout=30)
            elif filepath.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
                subprocess.run(['tar', '-xf', filepath, '-C', temp_dir], timeout=30)
            else:
                return threats
            
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    result = self.scan_file_for_viruses(full_path)
                    if result:
                        result['compressed_in'] = filepath
                        threats.append(result)
            
        except Exception as e:
            self.log(f"Error escaneando {filepath}: {e}", "ERROR")
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        
        return threats
    
    def scan_apk_file(self, filepath):
        threats = []
        temp_dir = None
        
        try:
            temp_dir = tempfile.mkdtemp(prefix="apk_scan_")
            self.log(f"Escaneando APK: {filepath}")
            
            subprocess.run(['7z', 'x', filepath, f'-o{temp_dir}', '-y'], timeout=60)
            
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.dex') or file.endswith('.so') or file.endswith('.jar'):
                        full_path = os.path.join(root, file)
                        result = self.scan_file_for_viruses(full_path)
                        if result:
                            result['apk_file'] = filepath
                            threats.append(result)
            
            dex_files = list(Path(temp_dir).rglob("*.dex"))
            for dex in dex_files:
                with open(dex, 'rb') as f:
                    content = f.read(10240)
                    for pattern in self.virus_signatures.get("patterns", []):
                        try:
                            if re.search(pattern, content.decode('utf-8', errors='ignore')):
                                threats.append({
                                    'type': 'apk_suspicious_code',
                                    'apk_file': filepath,
                                    'file': str(dex),
                                    'pattern': str(pattern),
                                    'severity': 'high'
                                })
                        except:
                            pass
            
        except Exception as e:
            self.log(f"Error escaneando APK {filepath}: {e}", "ERROR")
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        
        return threats
    
    def monitor_downloads(self):
        self.log("Monitoreando descargas recientes...")
        download_dirs = [
            '/home/agdala/Descargas',
            '/home/agdala/Downloads',
            '/tmp'
        ]
        
        threats_found = []
        
        for ddir in download_dirs:
            if not os.path.exists(ddir):
                continue
            
            try:
                files = os.listdir(ddir)
                for f in files:
                    filepath = os.path.join(ddir, f)
                    
                    if not os.path.isfile(filepath):
                        continue
                    
                    if any(filepath.endswith(ext) for ext in ['.zip', '.rar', '.7z', '.tar', '.tar.gz', '.tgz', '.tar.bz2']):
                        threats = self.scan_compressed_file(filepath)
                        if threats:
                            threats_found.extend(threats)
                            for t in threats:
                                self.show_notification(
                                    "¡Archivo Comprimido Sospechoso!",
                                    f"Se detectó: {t.get('type')} en {filepath}\nEl archivo será eliminado."
                                )
                                try:
                                    os.remove(filepath)
                                    self.log(f"Archivo comprimido eliminado: {filepath}", "ACTION")
                                except:
                                    pass
                    
                    elif filepath.endswith('.apk'):
                        threats = self.scan_apk_file(filepath)
                        if threats:
                            threats_found.extend(threats)
                            for t in threats:
                                self.show_notification(
                                    "¡APK Sospechosa!",
                                    f"Se detectó código malicioso en {filepath}\nLa APK será eliminada."
                                )
                                try:
                                    os.remove(filepath)
                                    self.log(f"APK eliminada: {filepath}", "ACTION")
                                except:
                                    pass
                    
                    else:
                        result = self.scan_file_for_viruses(filepath)
                        if result:
                            threats_found.append(result)
                            self.show_notification(
                                "¡Archivo Sospechoso!",
                                f"Se detectó: {result.get('type')} en {filepath}\nEl archivo será eliminado."
                            )
                            try:
                                os.remove(filepath)
                                self.log(f"Archivo eliminado: {filepath}", "ACTION")
                            except:
                                pass
            
            except Exception as e:
                self.log(f"Error monitoreando {ddir}: {e}", "ERROR")
        
        return threats_found
    
    def deep_scan_directory(self, directory, max_files=1000):
        self.log(f"Escaneando directorio: {directory}")
        threats = []
        file_count = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file_count >= max_files:
                        break
                    filepath = os.path.join(root, file)
                    result = self.scan_file_for_viruses(filepath)
                    if result:
                        threats.append(result)
                    file_count += 1
                if file_count >= max_files:
                    break
        except:
            pass
        
        return threats
    
    def check_network_connections(self):
        self.log("Analizando conexiones de red...")
        suspicious = []
        
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED' and conn.raddr:
                ip = conn.raddr.ip
                port = conn.raddr.port
                pid = conn.pid
                
                if port in self.known_threats["suspicious_ports"]:
                    suspicious.append({
                        'type': 'suspicious_port',
                        'ip': ip,
                        'port': port,
                        'pid': pid,
                        'severity': 'medium'
                    })
                    self.suspicious_ips.add(ip)
                
                if port in [4444, 31337, 1337]:
                    suspicious.append({
                        'type': 'possible_backdoor_port',
                        'ip': ip,
                        'port': port,
                        'pid': pid,
                        'severity': 'critical'
                    })
        
        if suspicious:
            self.threats_found.extend(suspicious)
            self.log(f"Encontradas {len(suspicious)} conexiones sospechosas", "WARNING")
        
        return suspicious
    
    def check_processes(self):
        self.log("Analizando procesos en ejecución...")
        suspicious = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                proc_info = proc.info
                proc_name = proc_info['name'].lower() if proc_info['name'] else ""
                cmdline = ' '.join(proc_info['cmdline']).lower() if proc_info['cmdline'] else ""
                
                for tool in self.known_threats["pentesting_tools"]:
                    if proc_name == tool or f"/{tool}" in proc_name or tool in cmdline.split():
                        suspicious.append({
                            'type': 'pentesting_tool_detected',
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'tool': tool,
                            'severity': 'high'
                        })
                
                for virus in self.known_threats["virus_names"]:
                    import re
                    if re.search(r'\b' + re.escape(virus) + r'\b', proc_name) or re.search(r'\b' + re.escape(virus) + r'\b', cmdline):
                        suspicious.append({
                            'type': 'virus_process',
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'virus_type': virus,
                            'severity': 'critical'
                        })
                
                if proc_info['cpu_percent'] and proc_info['cpu_percent'] > 80:
                    suspicious.append({
                        'type': 'high_cpu_usage',
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'cpu': proc_info['cpu_percent'],
                        'severity': 'low'
                    })
                
                if 'xmrig' in proc_name or 'minerd' in proc_name or 'cryptominer' in cmdline:
                    suspicious.append({
                        'type': 'cryptominer',
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'severity': 'critical'
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if suspicious:
            self.threats_found.extend(suspicious)
            self.log(f"Encontrados {len(suspicious)} procesos sospechosos", "WARNING")
        
        return suspicious
    
    def check_email_spam(self):
        self.log("Verificando indicadores de spam...")
        spam_threats = []
        
        mail_dirs = ['/var/mail', '/home/agdala/Mail', '/home/agdala/.thunderbird']
        
        for mail_dir in mail_dirs:
            if os.path.exists(mail_dir):
                try:
                    result = subprocess.run(['grep', '-r', '-l', r'spam\|phishing\|lottery', mail_dir],
                                          capture_output=True, text=True, timeout=10)
                    if result.stdout:
                        spam_threats.append({
                            'type': 'spam_email_found',
                            'location': mail_dir,
                            'files': result.stdout.strip().split('\n')[:5],
                            'severity': 'medium'
                        })
                except:
                    pass
        
        if spam_threats:
            self.threats_found.extend(spam_threats)
        
        return spam_threats
    
    def check_ddos_indicators(self):
        self.log("Verificando indicadores de DDoS...")
        ddos_threats = []
        
        try:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            connection_counts = defaultdict(int)
            
            for line in result.stdout.split('\n'):
                if 'ESTABLISHED' in line or 'SYN_RECV' in line:
                    parts = line.split()
                    if len(parts) > 4:
                        ip = parts[4].split(':')[0]
                        connection_counts[ip] += 1
            
            for ip, count in connection_counts.items():
                if count > 50:
                    ddos_threats.append({
                        'type': 'possible_ddos',
                        'ip': ip,
                        'connections': count,
                        'severity': 'high'
                    })
                    self.suspicious_ips.add(ip)
        except:
            pass
        
        if ddos_threats:
            self.threats_found.extend(ddos_threats)
            self.log(f"Detectados {len(ddos_threats)} posibles ataques DDoS", "ALERT")
        
        return ddos_threats
    
    def check_open_ports(self):
        self.log("Verificando puertos abiertos...")
        try:
            result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
            open_ports = []
            for line in result.stdout.split('\n'):
                if 'LISTEN' in line:
                    parts = line.split()
                    if len(parts) > 4:
                        addr_port = parts[4]
                        open_ports.append(addr_port)
            self.log(f"Puertos abiertos detectados: {len(open_ports)}")
            return open_ports
        except Exception as e:
            self.log(f"Error verificando puertos: {e}", "ERROR")
            return []
    
    def block_ip(self, ip):
        if ip in self.blocked_ips:
            return
        try:
            subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], 
                          capture_output=True, check=True)
            self.blocked_ips.add(ip)
            self.log(f"IP bloqueada: {ip}", "ALERT")
        except Exception as e:
            self.log(f"No se pudo bloquear IP {ip}: {e}", "ERROR")
    
    def quarantine_file(self, filepath):
        quarantine_dir = self.base_path / "quarantine"
        quarantine_dir.mkdir(exist_ok=True)
        
        try:
            import shutil
            dest = quarantine_dir / os.path.basename(filepath)
            shutil.move(filepath, dest)
            self.quarantined_files.append(str(filepath))
            self.log(f"Archivo en cuarentena: {filepath}", "ACTION")
            return True
        except Exception as e:
            self.log(f"Error en cuarentena: {e}", "ERROR")
            return False
    
    def scan_for_rootkits(self):
        self.log("Verificando posibles rootkits...")
        suspicious_files = []
        
        suspicious_paths = ['/tmp', '/dev/shm', '/var/tmp', '/proc/self/fd']
        for path in suspicious_paths:
            if os.path.exists(path):
                try:
                    for item in os.listdir(path):
                        full_path = os.path.join(path, item)
                        try:
                            if os.path.isfile(full_path):
                                size = os.path.getsize(full_path)
                                if size > 1024 * 1024:
                                    suspicious_files.append(full_path)
                                    virus_check = self.scan_file_for_viruses(full_path)
                                    if virus_check:
                                        self.threats_found.append(virus_check)
                        except:
                            continue
                except:
                    continue
        
        if suspicious_files:
            self.threats_found.append({
                'type': 'suspicious_files',
                'files': suspicious_files,
                'severity': 'medium'
            })
        
        return suspicious_files
    
    def check_system_integrity(self):
        self.log("Verificando integridad del sistema...")
        critical_files = [
            '/etc/passwd', '/etc/shadow', '/etc/sudoers', '/etc/ssh/sshd_config',
            '/etc/crontab', '/etc/profile', '/root/.bashrc', '/home/agdala/.bashrc'
        ]
        changes = []
        
        integrity_db = self.base_path / "integrity_db.json"
        current_hashes = {}
        
        for file in critical_files:
            if os.path.exists(file):
                hasher = hashlib.md5()
                with open(file, 'rb') as f:
                    hasher.update(f.read())
                current_hashes[file] = hasher.hexdigest()
        
        if integrity_db.exists():
            with open(integrity_db) as f:
                old_hashes = json.load(f)
                for file, old_hash in old_hashes.items():
                    if file in current_hashes and current_hashes[file] != old_hash:
                        changes.append({'file': file, 'status': 'modified', 'severity': 'high'})
        
        with open(integrity_db, 'w') as f:
            json.dump(current_hashes, f)
        
        if changes:
            self.threats_found.extend(changes)
            self.log(f"Integritad comprometida: {len(changes)} archivos modificados", "CRITICAL")
        
        return changes
    
    def check_failed_logins(self):
        self.log("Verificando intentos de login fallidos...")
        try:
            result = subprocess.run(['lastb', '-n', '50'], capture_output=True, text=True)
            failed = len([l for l in result.stdout.split('\n') if l.strip()])
            if failed > 5:
                self.threats_found.append({
                    'type': 'brute_force',
                    'count': failed,
                    'severity': 'high'
                })
                self.log(f"Posible ataque de fuerza bruta: {failed} intentos fallidos", "ALERT")
            return failed
        except:
            return 0
    
    def check_arp_spoofing(self):
        self.log("Verificando ARP spoofing...")
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            macs = []
            for line in result.stdout.split('\n'):
                if 'at' in line:
                    parts = line.split('at')
                    if len(parts) > 1:
                        mac = parts[1].strip().split()[0]
                        macs.append(mac)
            
            if len(macs) != len(set(macs)):
                self.threats_found.append({
                    'type': 'possible_arp_spoofing',
                    'severity': 'critical'
                })
                self.log("Posible ARP spoofing detectado!", "CRITICAL")
        except:
            pass
    
    def check_dns_poisoning(self):
        self.log("Verificando DNS poisoning...")
        try:
            with open('/etc/resolv.conf') as f:
                content = f.read()
                if '8.8.8.8' not in content and '1.1.1.1' not in content:
                    if len(content.strip()) > 0:
                        self.threats_found.append({
                            'type': 'suspicious_dns',
                            'content': content[:200],
                            'severity': 'medium'
                        })
        except:
            pass
    
    def auto_repel(self):
        self.log("Ejecutando contramedidas automáticas...")
        
        for threat in self.threats_found:
            if threat.get('severity') in ['high', 'critical']:
                if threat.get('type') == 'suspicious_process' or threat.get('type') == 'virus_process':
                    try:
                        os.kill(threat['pid'], signal.SIGKILL)
                        self.log(f"Proceso terminado: {threat.get('name', 'unknown')} (PID: {threat['pid']})", "ACTION")
                    except:
                        pass
                
                elif threat.get('type') == 'brute_force':
                    self.log("Activando protección contra fuerza bruta", "ACTION")
                    try:
                        subprocess.run(['iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '22', '-m', 'state', '--state', 'NEW', '-m', 'recent', '--set'], capture_output=True)
                        subprocess.run(['iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '22', '-m', 'state', '--state', 'NEW', '-m', 'recent', '--update', '--seconds', '60', '--hitcount', '4', '-j', 'DROP'], capture_output=True)
                    except:
                        pass
                
                elif threat.get('type') == 'possible_ddos':
                    self.block_ip(threat.get('ip'))
                
                elif threat.get('type') in ['virus_md5_match', 'virus_pattern_match', 'virus_known']:
                    filepath = threat.get('file')
                    if filepath:
                        self.quarantine_file(filepath)
                
                elif threat.get('ip'):
                    self.block_ip(threat.get('ip'))
    
    def generate_report(self):
        timestamp = datetime.datetime.now()
        report = {
            'timestamp': timestamp.isoformat(),
            'hostname': socket.gethostname(),
            'threats_detected': len(self.threats_found),
            'threats': self.threats_found,
            'blocked_ips': list(self.blocked_ips),
            'quarantined_files': self.quarantined_files,
            'system_status': 'COMPROMISED' if any(t.get('severity') in ['high', 'critical'] for t in self.threats_found) else 'SECURE'
        }
        
        report_file = self.report_path / f"report_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.update_readme(report)
        return report
    
    def update_readme(self, report):
        status_emoji = "🚨" if report['system_status'] == 'COMPROMISED' else "✅"
        
        content = f"""# Security AI Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Estado del Sistema: {status_emoji} {report['system_status']}

### Resumen
- **Hostname:** {report['hostname']}
- **Amenazas detectadas:** {report['threats_detected']}
- **IPs bloqueadas:** {len(report['blocked_ips'])}
- **Archivos en cuarentena:** {len(report['quarantined_files'])}

### Amenazas Encontradas
"""
        
        if report['threats']:
            for threat in report['threats']:
                severity = threat.get('severity', 'unknown').upper()
                threat_type = threat.get('type', 'unknown').replace('_', ' ').title()
                content += f"\n#### [{severity}] {threat_type}\n"
                for key, value in threat.items():
                    if key not in ['type', 'severity']:
                        if isinstance(value, list):
                            content += f"- **{key}:** {', '.join(map(str, value[:5]))}\n"
                        else:
                            content += f"- **{key}:** {value}\n"
        else:
            content += "\nNo se encontraron amenazas.\n"
        
        content += f"\n### IPs Bloqueadas\n"
        if report['blocked_ips']:
            for ip in report['blocked_ips']:
                content += f"- {ip}\n"
        else:
            content += "Ninguna IP bloqueada.\n"
        
        content += f"\n### Archivos en Cuarentena\n"
        if report['quarantined_files']:
            for file in report['quarantined_files']:
                content += f"- {file}\n"
        else:
            content += "Ninguno.\n"
        
        content += f"\n---\n*Generado por Security AI - {datetime.datetime.now().isoformat()}*\n"
        
        with open(self.readme_path, 'w') as f:
            f.write(content)
    
    def run_scan(self):
        self.log("=== Iniciando escaneo de seguridad COMPLETO ===", "START")
        self.threats_found = []
        
        self.check_network_connections()
        self.check_processes()
        self.check_open_ports()
        self.scan_for_rootkits()
        self.check_system_integrity()
        self.check_failed_logins()
        self.check_email_spam()
        self.check_ddos_indicators()
        self.check_arp_spoofing()
        self.check_dns_poisoning()
        
        home_scan = self.deep_scan_directory('/home/agdala', max_files=500)
        if home_scan:
            self.threats_found.extend(home_scan)
        
        download_threats = self.monitor_downloads()
        if download_threats:
            self.threats_found.extend(download_threats)
        
        if self.threats_found:
            self.auto_repel()
        
        report = self.generate_report()
        self.save_state()
        
        self.log("=== Escaneo completado ===", "COMPLETE")
        return report

if __name__ == "__main__":
    ai = SecurityAI()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--daemon":
            while True:
                ai.run_scan()
                time.sleep(3600)
        elif sys.argv[1] == "--report":
            report = ai.run_scan()
            print(json.dumps(report, indent=2))
        elif sys.argv[1] == "--quick":
            ai.check_network_connections()
            ai.check_processes()
            report = ai.generate_report()
            print(json.dumps(report, indent=2))
    else:
        report = ai.run_scan()
        print(json.dumps(report, indent=2))
