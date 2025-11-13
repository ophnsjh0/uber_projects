import requests
import json

HOST = "http://192.168.74.131/command-api"   # eAPI URL
USERNAME = "admin"
PASSWORD = "admin"

# 테스트용 단일 명령
payload = {
    "jsonrpc": "2.0",
    "method": "runCmds",
    "params": {
        "version": 1,
        "cmds": ["show interfaces status"],
        "format": "text"
    },
    "id": 1
}

def test_eapi():
    try:
        response = requests.post(
            HOST,
            data=json.dumps(payload),
            auth=(USERNAME, PASSWORD),
            headers={"Content-Type": "application/json"},
            verify=False,           # self-signed 인증서일 때 필수
            timeout=5
        )

        # 응답 출력
        print("HTTP Status:", response.status_code)
        print("----- Response -----")
        print(response.text)

    except Exception as e:
        print("[!] ERROR:", e)

if __name__ == "__main__":
    test_eapi()
