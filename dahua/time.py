Adjust time synchrounizingly
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
import concurrent.futures

# --- CONFIGURATION ---
# List all your Camera/NVR IPs here
IP_LIST = [
    "10.175.57.81",
    # "10.175.57.82",
    # "10.175.57.83",
    # Add as many as you need...
]

USER = "admin"
PASS = "IT@cam!@#"
TIMEOUT = 5 # Seconds to wait before giving up on a camera

def sync_camera_time(ip):
    # 1. Get current system time formatted for Dahua (YYYY-MM-DD HH:MM:SS)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Prepare the URL
    url = f"http://{ip}/cgi-bin/global.cgi"
    params = {
        "action": "setCurrentTime",
        "time": now
    }
    
    try:
        # 3. Send the request
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
    
    # Use ThreadPoolExecutor to run syncs in parallel
    # max_workers=20 means 20 cameras will be updated at the exact same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(sync_camera_time, IP_LIST)

if __name__ == "__main__":
    run_mass_sync()


