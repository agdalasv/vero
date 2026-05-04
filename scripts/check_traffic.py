#!/usr/bin/env python3
import subprocess
import json
import datetime
from collections import defaultdict

class TrafficMonitor:
    def __init__(self):
        self.connections = defaultdict(int)
        self.packet_count = 0
        
    def get_connections(self):
        try:
            result = subprocess.run(['ss', '-tun'], capture_output=True, text=True)
            lines = result.stdout.split('\n')[1:]
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        self.connections[parts[4]] += 1
            return dict(self.connections)
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_traffic(self):
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'connections': self.get_connections(),
            'total_unique': len(self.connections)
        }
        return report

if __name__ == "__main__":
    monitor = TrafficMonitor()
    report = monitor.analyze_traffic()
    print(json.dumps(report, indent=2))
