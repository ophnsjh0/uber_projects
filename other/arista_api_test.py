import requests
import json

url = "http://192.168.74.130:32769/command-api"
headers = {"Content-Type": "application/json"}
payload = {
    "jsonrpc": "2.0",
    "method": "runCmds",
    "params": {
        "version": 1,
        "cmds": ["enable", "show interfaces"]
    },
    "id": "1"
}

response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=('admin', '1234qwer'))
print(response.json())
