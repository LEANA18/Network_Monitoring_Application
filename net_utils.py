import socket
import subprocess
import os
import re

def get_current_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unavailable"

def check_internet():
    return os.system("ping -n 1 8.8.8.8 >nul 2>&1") == 0  # For Windows

def get_wifi_strength():
    try:
        output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        match = re.search(r'Signal\s*:\s*(\d+)%', output)
        return int(match.group(1)) if match else None
    except:
        return None