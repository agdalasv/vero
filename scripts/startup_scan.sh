#!/bin/bash

LOG="/home/agdala/documentos/security_ai/startup.log"
echo "=== Security AI Startup Scan - $(date) ===" >> "$LOG"

python3 /home/agdala/documentos/security_ai/security_ai.py --report >> "$LOG" 2>&1

echo "Startup scan completed at $(date)" >> "$LOG"
