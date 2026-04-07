import pandas as pd
import requests
from requests.auth import HTTPDigestAuth
from concurrent.futures import ThreadPoolExecutor

# --- FIXED CONFIGURATION ---
USERNAME = "admin"
PASSWORD = "IT@cam!@#"
CHANNEL = 0
FILE_NAME = "cameras.xlsx"
# ---------------------------

def update_single_camera(row):
    """
    Takes a row from Excel and performs the update.
    """
    # Extract IP and Name from the Excel columns
    ip = str(row['ip']).strip()
    name = str(row['name']).strip()
    
    url = f"http://{ip}/cgi-bin/configManager.cgi"
    params = {
        "action": "setConfig",
        f"ChannelTitle[{CHANNEL}].Name": name
    }
    
    try:
        response = requests.get(
            url, 
            params=params, 
            auth=HTTPDigestAuth(USERNAME, PASSWORD), 
            timeout=10  # Increased timeout for better reliability
        )
        
        # Dahua specific check: Status 200 is good, but we need "OK" in the body
        if response.status_code == 200:
            if "OK" in response.text:
                return f"[SUCCESS] {ip}: Name set to {name}"
            else:
                # If it says 'Error', check if CGI is enabled in camera settings
                return f"[FAILED] {ip}: Camera returned '{response.text.strip()}'"
        else:
            return f"[FAILED] {ip}: Status {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"[ERROR] {ip}: {str(e)}"

def batch_process(max_workers=20):
    """
    Reads the Excel file and manages the thread pool.
    """
    try:
        # Read only 'ip' and 'name' columns from the Excel file
        df = pd.read_excel(FILE_NAME, usecols=['ip', 'name'])
        camera_list = df.to_dict('records')
    except FileNotFoundError:
        print(f"Error: '{FILE_NAME}' not found. Please create it in this folder.")
        return
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return

    print(f"Starting batch update for {len(camera_list)} cameras...\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(update_single_camera, camera_list))
    
    print("\n--- FINAL REPORT ---")
    for result in results:
        print(result)

if __name__ == "__main__":
    # Adjust max_workers based on your network capacity
    batch_process(max_workers=20)


















# import requests
# from requests.auth import HTTPDigestAuth
# from concurrent.futures import ThreadPoolExecutor

# # Configuration: List of cameras [IP, Username, Password, Channel, New Name]
# CAMERAS = [
#     ["10.175.58.141", "admin", "IT@cam!@#", 0, "1-1- Enterance 1"],
#     ["10.175.58.135", "admin", "IT@cam!@#", 0, "1-2- Enterance 2"],
#     ["10.175.58.99", "admin", "IT@cam!@#", 0, "1-3- Offers 1"],
#     # Add hundreds more here...
# ]

# def update_single_camera(cam_info):
#     ip, user, pwd, channel, name = cam_info
#     url = f"http://{ip}/cgi-bin/configManager.cgi"
#     params = {
#         "action": "setConfig",
#         f"ChannelTitle[{channel}].Name": name
#     }
    
#     try:
#         response = requests.get(
#             url, 
#             params=params, 
#             auth=HTTPDigestAuth(user, pwd), 
#             timeout=5  # Short timeout so one dead cam doesn't hang the script
#         )
        
#         if response.status_code == 200 and "OK" in response.text:
#             return f"[SUCCESS] {ip}: Name set to {name}"
#         else:
#             return f"[FAILED] {ip}: Status {response.status_code}"
            
#     except requests.exceptions.RequestException as e:
#         return f"[ERROR] {ip}: {str(e)}"

# def batch_process(camera_list, max_workers=10):
#     print(f"Starting batch update for {len(camera_list)} cameras...\n")
    
#     # max_workers determines how many cameras to hit at once
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         results = list(executor.map(update_single_camera, camera_list))
    
#     for result in results:
#         print(result)

# if __name__ == "__main__":
#     # Adjust max_workers based on your network capacity
#     batch_process(CAMERAS, max_workers=20)

























# import requests
# from requests.auth import HTTPDigestAuth

# def change_dahua_name(ip, username, password, channel=0, new_name="New_Camera_Name"):
#     # Dahua uses 0-based indexing for channels (Channel 1 = index 0)
#     # The 'set' command updates the ChannelTitle name
#     url = f"http://{ip}/cgi-bin/configManager.cgi"
#     params = {
#         "action": "setConfig",
#         f"ChannelTitle[{channel}].Name": new_name
#     }

#     try:
#         # Dahua almost exclusively uses Digest Authentication
#         response = requests.get(
#             url, 
#             params=params, 
#             auth=HTTPDigestAuth(username, password),
#             timeout=10
#         )
        
#         if response.status_code == 200 and "OK" in response.text:
#             print(f"Success! Name changed to: {new_name}")
#         else:
#             print(f"Error: {response.status_code}")
#             print(f"Response text: {response.text}")
            
#     except Exception as e:
#         print(f"Request failed: {e}")

# # Usage
# CAM_IP = "10.175.58.141"
# USER = "admin"
# PASS = "IT@cam!@#"
# change_dahua_name(CAM_IP, USER, PASS, channel=0, new_name="1-1- Enterance 1")



























# import requests
# from requests.auth import HTTPDigestAuth

# # Use the 'VideoWidget' structure which is more 'Implemented' on newer Dahua
# def update_dahua_name(ip, user, pw, name):
#     url = f"http://{ip}/cgi-bin/configManager.cgi"
    
#     # We use VideoWidget because it controls the OSD (On Screen Display) name
#     params = {
#         'action': 'setConfig',
#         'VideoWidget[0].CustomTitle[0].Text': name,
#         'VideoWidget[0].CustomTitle[0].EncodeMode': 'UTF-8'
#     }
    
#     try:
#         r = requests.get(url, params=params, auth=HTTPDigestAuth(user, pw), timeout=15)
#         if "OK" in r.text:
#             print("Success!")
#         else:
#             print(f"Server replied: {r.text}")
#     except Exception as e:
#         print(f"Error: {e}")

# update_dahua_name('10.175.58.141', 'admin', 'IT@cam!@#', 'Office_Cam')


# set_name_robust("10.175.58.141", "admin", "IT@cam!@#", 0, "1-1- Enterance 5")

















# import requests
# from requests.auth import HTTPDigestAuth

# def set_name_robust(ip, user, pw, idx, name):
#     session = requests.Session()
#     session.auth = HTTPDigestAuth(user, pw)
    
#     url = f"http://{ip}/cgi-bin/configManager.cgi"
#     params = {'action': 'setConfig', f'ChannelTitle[{idx}].Name': name}
    
#     try:
#         # We use a longer timeout here
#         response = session.get(url, params=params, timeout=30)
#         print(f"Status: {response.status_code}, Body: {response.text}")
#     except requests.exceptions.ReadTimeout:
#         print("Error: The camera took too long to answer. Try rebooting the camera.")
#     except requests.exceptions.ConnectionError:
#         print("Error: Could not connect to the camera. Check the IP and Port.")

# set_name_robust("10.175.58.141", "admin", "IT@cam!@#", 0, "1-1- Enterance 5")