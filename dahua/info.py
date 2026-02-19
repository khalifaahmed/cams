
import requests
from requests.auth import HTTPDigestAuth
import re
import csv
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
subnet_prefix = "10.175.57"
admin_user = "admin"
admin_pass = "IT@cam!@#"
output_file = "dahua_camera_results.csv"

def scan_dahua_camera(ip):
    auth = HTTPDigestAuth(admin_user, admin_pass)
    timeout = 2
    
    try:
        # 1. Get System Info (for Serial Number)
        # Dahua path: magicBox.cgi?action=getSystemInfo
        info_url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
        r_info = requests.get(info_url, auth=auth, timeout=timeout)
        
        if r_info.status_code == 200:
            # Extract Serial using Regex
            # Typical response: serialNumber=1D02845PAZXXXXX
            s_match = re.search(r'serialNumber=(.*)', r_info.text)
            serial = s_match.group(1).strip() if s_match else "Unknown"
            
            # 2. Get Network Config (for MAC Address)
            # Dahua path: configManager.cgi?action=getConfig&name=Network
            net_url = f"http://{ip}/cgi-bin/configManager.cgi?action=getConfig&name=Network"
            r_net = requests.get(net_url, auth=auth, timeout=timeout)
            
            mac = "Not Found"
            if r_net.status_code == 200:
                # Typical response: table.Network.eth0.PhysicalAddress=bc:32:d5:xx:xx:xx
                m_match = re.search(r'PhysicalAddress=(.*)', r_net.text)
                if m_match:
                    mac = m_match.group(1).strip().upper()

            return {"IP Address": ip, "MAC Address": mac, "Serial Number": serial}
    except:
        pass
    return None

# --- EXECUTION ---
print(f"Scanning Dahua Subnet {subnet_prefix}.1 to .255...")
print(f"{'IP Address':<15} | {'MAC Address':<18} | {'Serial Number'}")
print("-" * 80)

ips = [f"{subnet_prefix}.{i}" for i in range(1, 256)]
found_cameras = []

with ThreadPoolExecutor(max_workers=30) as executor:
    results = executor.map(scan_dahua_camera, ips)
    for res in results:
        if res:
            found_cameras.append(res)
            print(f"{res['IP Address']:<15} | {res['MAC Address']:<18} | {res['Serial Number']}")

# Write to CSV
if found_cameras:
    keys = found_cameras[0].keys()
    with open(output_file, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(found_cameras)
    print("-" * 80)
    print(f"Success! {len(found_cameras)} Dahua cameras saved to {output_file}")
else:
    print("\nNo Dahua cameras found.")









#=================================================================================================================================================
#works on a whole subnet

# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# import re

# def scan_subnet(prefix, start, end, user, pw):
#     auth = HTTPDigestAuth(user, pw)
#     timeout = 1.5  # Short timeout since we are walking one-by-one
    
#     print(f"Starting walk-through for subnet {prefix}.{start}-{end}...")
#     print(f"{'IP Address':<15} | {'Status':<10} | {'MAC Address':<18} | {'Serial Number'}")
#     print("-" * 80)

#     for i in range(start, end + 1):
#         ip = f"{prefix}.{i}"
#         # Visual indicator that the script is working
#         print(f"[{ip}] Scanning...", end="\r")

#         # 1. Try Hikvision
#         try:
#             hik_url = f"http://{ip}/ISAPI/System/deviceInfo"
#             r = requests.get(hik_url, auth=auth, timeout=timeout)
#             if r.status_code == 200:
#                 ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
#                 root = ET.fromstring(r.content)
#                 serial = root.find(".//ns:serialNumber", ns).text
                
#                 # Get MAC
#                 r_net = requests.get(f"http://{ip}/ISAPI/System/Network/interfaces/1", auth=auth, timeout=timeout)
#                 mac = ET.fromstring(r_net.content).find(".//ns:macAddress", ns).text if r_net.status_code == 200 else "Unknown"
                
#                 print(f"{ip:<15} | Hikvision  | {mac:<18} | {serial}")
#                 continue
#         except:
#             pass

#         # 2. Try Dahua
#         try:
#             dah_url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
#             r = requests.get(dah_url, auth=auth, timeout=timeout)
#             if r.status_code == 200:
#                 s_match = re.search(r'serialNumber=(.*)', r.text)
#                 serial = s_match.group(1).strip() if s_match else "Unknown"
                
#                 # Get MAC
#                 r_net = requests.get(f"http://{ip}/cgi-bin/configManager.cgi?action=getConfig&name=Network", auth=auth, timeout=timeout)
#                 m_match = re.search(r'PhysicalAddress=(.*)', r_net.text)
#                 mac = m_match.group(1).strip() if m_match else "Unknown"

#                 print(f"{ip:<15} | Dahua      | {mac:<18} | {serial}")
#                 continue
#         except:
#             pass

#     print("\n--- Scan Complete ---")

# # --- SETTINGS ---
# scan_subnet("10.175.57", 1, 255, "admin", "IT@cam!@#")




#===================================================================================================================================================




#very nice this code

# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# import re
# from concurrent.futures import ThreadPoolExecutor

# def get_camera_details(ip):
#     # --- CONFIGURATION ---
#     user = "admin"
#     pw = "IT@cam!@#"
#     auth = HTTPDigestAuth(user, pw)
#     timeout = 2 #Low timeout for faster scanning
    
#     # 1. HIKVISION ATTEMPT
#     try:
#         hik_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         r = requests.get(hik_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
#             root = ET.fromstring(r.content)
#             serial = root.find(".//ns:serialNumber", ns).text
            
#             # Get MAC
#             r_net = requests.get(f"http://{ip}/ISAPI/System/Network/interfaces/1", auth=auth, timeout=timeout)
#             mac = "Unknown"
#             if r_net.status_code == 200:
#                 mac = ET.fromstring(r_net.content).find(".//ns:macAddress", ns).text
            
#             return f"{ip:<15} | Hikvision  | {mac:<18} | {serial}"
#     except:
#         pass

#     # 2. DAHUA ATTEMPT
#     try:
#         dah_url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
#         r = requests.get(dah_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             s_match = re.search(r'serialNumber=(.*)', r.text)
#             serial = s_match.group(1).strip() if s_match else "Unknown"
            
#             # Get MAC
#             r_net = requests.get(f"http://{ip}/cgi-bin/configManager.cgi?action=getConfig&name=Network", auth=auth, timeout=timeout)
#             m_match = re.search(r'PhysicalAddress=(.*)', r_net.text)
#             mac = m_match.group(1).strip() if m_match else "Unknown"

#             return f"{ip:<15} | Dahua      | {mac:<18} | {serial}"
#     except:
#         pass

#     return None # Return nothing if no camera found

# # --- MAIN EXECUTION ---
# subnet_prefix = "10.175.57"
# ips = [f"{subnet_prefix}.{i}" for i in range(5, 251)]

# print(f"{'IP Address':<15} | {'Brand':<10} | {'MAC Address':<18} | {'Serial Number'}")
# print("-" * 80)

# # Using 20 threads to scan simultaneously
# with ThreadPoolExecutor(max_workers=20) as executor:
#     results = executor.map(get_camera_details, ips)

# # Print only the successful hits
# for res in results:
#     if res:
#         print(res)





















# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# import re

# def get_camera_details(ip, user, pw):
#     auth = HTTPDigestAuth(user, pw)
#     timeout = 3 # Shorter timeout for faster batch scanning
    
#     # --- 1. HIKVISION ATTEMPT ---
#     try:
#         hik_info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         r = requests.get(hik_info_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
#             root = ET.fromstring(r.content)
#             serial = root.find(".//ns:serialNumber", ns).text
            
#             # Get MAC
#             hik_net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
#             r_net = requests.get(hik_net_url, auth=auth, timeout=timeout)
#             mac = "Unknown"
#             if r_net.status_code == 200:
#                 net_root = ET.fromstring(r_net.content)
#                 mac = net_root.find(".//ns:macAddress", ns).text
            
#             return {"ip": ip, "brand": "Hikvision", "serial": serial, "mac": mac}
#     except:
#         pass

#     # --- 2. DAHUA ATTEMPT ---
#     try:
#         dah_info_url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
#         r = requests.get(dah_info_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             serial = "Unknown"
#             s_match = re.search(r'serialNumber=(.*)', r.text)
#             if s_match: serial = s_match.group(1).strip()
            
#             # Get MAC
#             dah_net_url = f"http://{ip}/cgi-bin/configManager.cgi?action=getConfig&name=Network"
#             r_net = requests.get(dah_net_url, auth=auth, timeout=timeout)
#             mac = "Unknown"
#             m_match = re.search(r'PhysicalAddress=(.*)', r_net.text)
#             if m_match: mac = m_match.group(1).strip()

#             return {"ip": ip, "brand": "Dahua", "serial": serial, "mac": mac}
#     except:
#         pass

#     return {"ip": ip, "brand": "Failed", "serial": "N/A", "mac": "N/A"}

# # --- CONFIGURATION ---
# # Add all your camera IPs here
# camera_list = [
#     "10.175.57.81",
#     "10.175.57.82",
#     "10.175.57.83",
#     # Add more as needed
# ]

# username = "admin"
# password = "IT@cam!@#"

# # --- EXECUTION ---
# print(f"{'IP Address':<15} | {'Brand':<10} | {'MAC Address':<18} | {'Serial Number'}")
# print("-" * 80)

# for ip in camera_list:
#     result = get_camera_details(ip, username, password)
#     print(f"{result['ip']:<15} | {result['brand']:<10} | {result['mac']:<18} | {result['serial']}")





























# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# import re

# def get_camera_info(ip, user, pw):
#     auth = HTTPDigestAuth(user, pw)
#     timeout = 10
    
#     # --- 1. HIKVISION ATTEMPT ---
#     hik_info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#     hik_net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
    
#     try:
#         r = requests.get(hik_info_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
#             root = ET.fromstring(r.content)
#             serial = root.find(".//ns:serialNumber", ns).text
            
#             # Get MAC
#             r_net = requests.get(hik_net_url, auth=auth, timeout=timeout)
#             mac = "Unknown"
#             if r_net.status_code == 200:
#                 net_root = ET.fromstring(r_net.content)
#                 mac = net_root.find(".//ns:macAddress", ns).text
            
#             print(f"[{ip}] Brand: Hikvision")
#             print(f"Serial: {serial}")
#             print(f"MAC:    {mac}\n")
#             return
#     except:
#         pass

#     # --- 2. DAHUA ATTEMPT ---
#     dah_info_url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
#     dah_net_url = f"http://{ip}/cgi-bin/configManager.cgi?action=getConfig&name=Network"

#     try:
#         r = requests.get(dah_info_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             # Extract Serial from Dahua response text
#             serial = "Unknown"
#             s_match = re.search(r'serialNumber=(.*)', r.text)
#             if s_match: serial = s_match.group(1).strip()
            
#             # Extract MAC
#             r_net = requests.get(dah_net_url, auth=auth, timeout=timeout)
#             mac = "Unknown"
#             m_match = re.search(r'PhysicalAddress=(.*)', r_net.text)
#             if m_match: mac = m_match.group(1).strip()

#             print(f"[{ip}] Brand: Dahua")
#             print(f"Serial: {serial}")
#             print(f"MAC:    {mac}\n")
#             return
#     except:
#         pass

#     print(f"[{ip}] Failed: Connection error or unknown brand.")

# # Run
# get_camera_info("10.175.57.81", "admin", "IT@cam!@#")
















# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# import re

# def get_camera_info(ip, user, pw):
#     print(f"\n--- Checking Camera at {ip} ---")
#     auth = HTTPDigestAuth(user, pw)
#     timeout = 5

#     # 1. Hikvision Logic
#     hik_url = f"http://{ip}/ISAPI/System/deviceInfo"
#     hik_net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1" # Endpoint for MAC
    
#     try:
#         r = requests.get(hik_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             print("Brand Detected: Hikvision")
#             root = ET.fromstring(r.content)
#             ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
            
#             model = root.find(".//ns:model", ns).text if root.find(".//ns:model", ns) is not None else "Unknown"
            
#             # Get MAC Address
#             r_net = requests.get(hik_net_url, auth=auth, timeout=timeout)
#             mac = "Unknown"
#             if r_net.status_code == 200:
#                 net_root = ET.fromstring(r_net.content)
#                 mac = net_root.find(".//ns:macAddress", ns).text if net_root.find(".//ns:macAddress", ns) is not None else "Unknown"

#             print(f"Model: {model}")
#             print(f"MAC Address: {mac}")
#             return
#     except Exception:
#         pass

#     # 2. Dahua Logic
#     # Dahua uses magicBox.cgi for system info and configManager for network
#     dah_url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
#     dah_net_url = f"http://{ip}/cgi-bin/configManager.cgi?action=getConfig&name=Network"

#     try:
#         r = requests.get(dah_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             print("Brand Detected: Dahua")
            
#             # Get MAC using configManager
#             r_net = requests.get(dah_net_url, auth=auth, timeout=timeout)
#             mac = "Unknown"
#             if r_net.status_code == 200:
#                 # Use Regex to find MacAddress=XX:XX:XX...
#                 match = re.search(r'table\.Network\.eth0\.PhysicalAddress=(.*)', r_net.text)
#                 if match:
#                     mac = match.group(1).strip()

#             print(f"System Info: {r.text.strip()}")
#             print(f"MAC Address: {mac}")
#             return
#     except Exception:
#         pass

#     print("Could not detect camera brand or login failed.")

# # Run
# get_camera_info("10.175.57.81", "admin", "IT@cam!@#")

















# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET

# def get_camera_info(ip, user, pw):
#     print(f"\n--- Checking Camera at {ip} ---")
    
#     # 1. محاولة فحص Hikvision
#     hik_url = f"http://{ip}/ISAPI/System/deviceInfo"
#     try:
#         r = requests.get(hik_url, auth=HTTPDigestAuth(user, pw), timeout=5)
#         if r.status_code == 200:
#             print("Brand Detected: Hikvision")
#             root = ET.fromstring(r.content)
#             # استخراج البيانات من XML (مع التعامل مع الـ Namespace)
#             ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
#             model = root.find(".//ns:model", ns).text if root.find(".//ns:model", ns) is not None else "Unknown"
#             serial = root.find(".//ns:serialNumber", ns).text if root.find(".//ns:serialNumber", ns) is not None else "Unknown"
#             ver = root.find(".//ns:firmwareVersion", ns).text if root.find(".//ns:firmwareVersion", ns) is not None else "Unknown"
            
#             print(f"Model: {model}")
#             print(f"Serial: {serial}")
#             print(f"Firmware: {ver}")
#             return
#     except:
#         pass

#     # 2. محاولة فحص Dahua
#     dah_url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"
#     try:
#         r = requests.get(dah_url, auth=HTTPDigestAuth(user, pw), timeout=5)
#         if r.status_code == 200:
#             print("Brand Detected: Dahua")
#             # Dahua ترسل البيانات كنص عادي (Key=Value)
#             info = r.text
#             print(info.strip())
#             return
#     except:
#         pass

#     print("Could not detect camera brand or login failed.")

# # تشغيل الكود
# get_camera_info("10.175.57.81", "admin", "IT@cam!@#")