#!/bin/bash
cd /home/lucas/.openclaw/workspace
python3 phillies-intel-hub/email_scheduler.py 2>&1 | grep -v "Error fetching"
