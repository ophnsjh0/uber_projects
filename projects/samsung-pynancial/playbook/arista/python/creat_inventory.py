import os
import time
import json
import requests
from requests.auth import HTTPBasicAuth
import subprocess


DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
EAPI_PORT = 80
USERNAME = 'admin'
PASSWORD = 'admin'

def read_dnsmasq_leases():
    leases = []
    if not os.path.exists(DNSMASQ_LEASE_FILE):
        raise FileNotFoundError(f"{DNSMASQ_LEASE_FILE} not found.")
    
    with open(DNSMASQ_LEASE_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 3:
                lease = {
                    'expiry': parts[0],
                    'mac': parts[1],
                    'ip': parts[2],
                    'hostname': parts[3] if len(parts) >= 4 else None
                }
                leases.append(lease)
    return leases

def get_serial_from_device(ip):
    proxies = {
    "http": None,
    "https": None,
    }
    url = f"http://{ip}:{EAPI_PORT}/command-api"
    headers = {'Content-Type': 'application/json'}

    payload = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {
            "version": 1,
            "cmds": ["show version"],
            "format": "json"
        },
        "id": 1
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=10,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            proxies=proxies,
            verify=False
        )
        response.raise_for_status()
        result = response.json()
        serial = result['result'][0]['serialNumber']
        return serial
    except Exception as e:
        print(f"[!] Error fetching serial from {ip}: {e}")
        return None

def generate_inventory_ini(output_file='inventory.ini'):
    leases = read_dnsmasq_leases()

    lines = ["[arista_switches]"]

    for index, lease in enumerate(leases, start=1):
        ip = lease['ip']
        hostname = f"switch{index}"

        print(f"[*] Processing {hostname} ({ip})...")

        serial = get_serial_from_device(ip)

        if serial:
            lines.append(f"{hostname} ansible_host={ip} device_serial={serial}")
        else:
            print(f"[-] Failed to get serial for {ip}")

    lines.append("\n[arista_switches:vars]")
    lines.append("ansible_connection=network_cli")
    lines.append("ansible_network_os=arista.eos.eos")
    lines.append("ansible_user=admin")
    lines.append("ansible_password=admin")
    lines.append("ansible_become=true")
    lines.append("ansible_become_password=admin")
    lines.append("ansible_ssh_common_args='-o StrictHostKeyChecking=no'")
    lines.append("ansible_command_timeout=300")

    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))

    print(f"[+] inventory.ini 파일 생성 완료: {output_file}")

if __name__ == "__main__":
    generate_inventory_ini()
