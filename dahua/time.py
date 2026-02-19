Adjust time synchrounizingly
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
import concurrent.futures

# --- CONFIGURATION ---
IP_LIST = [
    "10.175.57.81",
    # "10.175.57.82",
    # "10.175.57.83",

]

USER = "admin"
PASS = "IT@cam!@#"
TIMEOUT = 5

def sync_camera_time(ip):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    url = f"http://{ip}/cgi-bin/global.cgi"
    params = {
        "action": "setCurrentTime",
        "time": now
    }
    
    try:
        response = requests.get(
            url, 
            params=params, 
            auth=HTTPDigestAuth(USER, PASS), 
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            print(f"[SUCCESS] {ip} synced to {now}")
        else:
            print(f"[FAILED] {ip} returned Status {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] {ip} is unreachable: {e}")

def run_mass_sync():
    print(f"Starting mass time sync for {len(IP_LIST)} devices...")
    
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(sync_camera_time, IP_LIST)

if __name__ == "__main__":
    run_mass_sync()


