#!/usr/bin/env python3

import subprocess
import json
import sys

def get_management_ip():
    try:
        result = subprocess.run(
            ['Cli', '-c', 'show interfaces Management1 | json'],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        interface = data.get('interfaces', {}).get('Management1', {})
        addresses = interface.get('interfaceAddress', [])
        if addresses:
            primary_ip = addresses[0].get('primaryIp', {}).get('address')
            if primary_ip:
                return primary_ip
        print("❌ Management1 IP address not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to retrieve management IP: {e}")
        sys.exit(1)

def write_startup_config(ip_address):
    config = f"""
!
hostname arista-switch
interface Management1
   ip address {ip_address}/24
   no shutdown
!
logging buffered 40000
!
clock timezone Asia/Seoul
!
username admin role network-admin secret admin
!
banner login
//////////////////////////////////////////////////////////////////////
//                                                                  //
//   - This system is to be logged in to or                         //
//     used only by specifically authorized personnel.              //
//   - Any unauthorized use of the system is unlawful, and may be   //
//     subject to civil and/or criminal penalties.                  //
//   - Any use of the system may be logged or monitored, and the    //
//     resulting logs may be used as evidence in court              //
//   - In logging in this system, we assume                         //
//     that you already agree our policy.                           //
//                                                                  //
//////////////////////////////////////////////////////////////////////
EOF
!
management console
   idle-timeout 5
!
aaa authentication login default local
!
management ssh
   enable
!
no ip icmp redirect
ip icmp rate-limit-unreachable 0
!
management api http-commands
   protocol http
   protocol https
   no shutdown
!
"""
    try:
        with open('/mnt/flash/startup-config', 'w') as f:
            f.write(config)
        print("✅ startup-config written successfully.")
    except Exception as e:
        print(f"❌ Failed to write startup-config: {e}")
        sys.exit(1)

def main():
    ip_address = get_management_ip()
    print(f"✅ Detected Management1 IP: {ip_address}")
    write_startup_config(ip_address)
    print("✅ ZTP configuration completed. The device will reboot with the new configuration.")

if __name__ == "__main__":
    main()
