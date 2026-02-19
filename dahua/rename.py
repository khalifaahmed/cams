import requests
from requests.auth import HTTPDigestAuth

# Configuration: IP and the desired Name
CAMERAS = {
    "10.175.57.81": "2-1-C.Service",
    # "10.175.57.82": "Server_Room",
    # "10.175.57.83": "Main_Lobby",
}

USER = "admin"
PASS = "IT@cam!@#"

def rename_camera(ip, new_name):
    url = f"http://{ip}/cgi-bin/configManager.cgi"
    params = {
        "action": "setConfig",
        "ChannelTitle[0].Name": new_name
    }
    
    try:
        response = requests.get(
            url, 
            params=params, 
            auth=HTTPDigestAuth(USER, PASS), 
            timeout=5
        )
        if response.status_code == 200 and "OK" in response.text:
            print(f"[SUCCESS] {ip} renamed to {new_name}")
        else:
            print(f"[FAILED] {ip} - Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] {ip} is unreachable: {e}")

if __name__ == "__main__":
    for ip, name in CAMERAS.items():
        rename_camera(ip, name)




















