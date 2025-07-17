import socket
import subprocess
import os
import re
import platform

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
  
    hosts = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]

    for host in hosts:
        response = os.system(f"ping -n 1 {host} >nul 2>&1") 
       
        if response == 0:
            return True, host 

    return False, None 

def get_wifi_strength():
    try:
        output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        match = re.search(r'Signal\s*:\s*(\d+)%', output)
        return int(match.group(1)) if match else None
    except:
        return None