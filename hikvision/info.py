# import requests
# from requests.auth import HTTPDigestAuth, HTTPBasicAuth
# import xml.etree.ElementTree as ET

# def test_single_camera(ip, user, pw):
#     protocols = [HTTPDigestAuth(user, pw), HTTPBasicAuth(user, pw)]
#     urls = {
#         "info": f"http://{ip}/ISAPI/System/deviceInfo",
#         "net": f"http://{ip}/ISAPI/System/Network/interfaces/1"
#     }
    
#     print(f"Checking {ip}...")

#     for auth_type in protocols:
#         try:
#             # Try to get Device Info
#             r = requests.get(urls["info"], auth=auth_type, timeout=3)
            
#             if r.status_code == 200:
#                 ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}
#                 root = ET.fromstring(r.content)
#                 serial = root.find(".//ns:serialNumber", ns).text
                
#                 # Get MAC
#                 r_net = requests.get(urls["net"], auth=auth_type, timeout=3)
#                 mac = "Unknown"
#                 if r_net.status_code == 200:
#                     mac = ET.fromstring(r_net.content).find(".//ns:macAddress", ns).text
                
#                 print(f"SUCCESS! Brand: Hikvision | MAC: {mac} | Serial: {serial}")
#                 return
#             elif r.status_code == 401:
#                 print(f"FAILED: 401 Unauthorized for {type(auth_type).__name__} (Wrong User/PW?)")
#             else:
#                 print(f"FAILED: Received Status Code {r.status_code}")
                
#         except requests.exceptions.ConnectTimeout:
#             print("FAILED: Connection Timeout (IP might be empty or firewall blocked)")
#             break # No point trying different auth if the IP is dead
#         except Exception as e:
#             print(f"ERROR: {e}")
#             break

# # Let's test just ONE known IP first to see why it's failing
# test_single_camera("10.175.57.81", "admin", "IT@cam!@#")

















# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# from concurrent.futures import ThreadPoolExecutor

# def scan_hikvision(ip):
#     # --- CONFIGURATION ---
#     user = "admin"
#     pw = "IT@cam!@#"
#     auth = HTTPDigestAuth(user, pw)
#     timeout = 2  # Seconds to wait per IP
    
#     # Hikvision API Endpoints
#     info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#     net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
#     ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}

#     try:
#         # 1. Check for device info & Serial
#         r = requests.get(info_url, auth=auth, timeout=timeout)
#         if r.status_code == 200:
#             root = ET.fromstring(r.content)
#             serial = root.find(".//ns:serialNumber", ns).text
            
#             # 2. Check for MAC address
#             r_net = requests.get(net_url, auth=auth, timeout=timeout)
#             mac = "Unknown"
#             if r_net.status_code == 200:
#                 net_root = ET.fromstring(r_net.content)
#                 mac = net_root.find(".//ns:macAddress", ns).text
            
#             # Formatting the result
#             return f"{ip:<15} | Hikvision | {mac:<18} | {serial}"
#     except Exception:
#         # Silently skip if it's not a Hikvision device or connection fails
#         pass
#     return None

# # --- MAIN EXECUTION ---
# subnet_prefix = "10.175.0"
# ips = [f"{subnet_prefix}.{i}" for i in range(1, 256)]

# print(f"Scanning Hikvision devices on {subnet_prefix}.x ...\n")
# print(f"{'IP Address':<15} | {'Brand':<9} | {'MAC Address':<18} | {'Serial Number'}")
# print("-" * 80)

# # max_workers=30 allows the script to 'walk' faster by checking 30 IPs at once
# with ThreadPoolExecutor(max_workers=30) as executor:
#     # map returns results in the order of the IPs provided
#     results = executor.map(scan_hikvision, ips)
    
#     for res in results:
#         if res:
#             print(res)

# print("-" * 80)
# print("Scan Complete.")










#==============================================================================================================================================================
#info for single camera

# import requests
# from requests.auth import HTTPDigestAuth


# ip = "10.175.0.62"
# admin_user = "admin"
# admin_pass = "IT@cam!@#"


# url = f"http://{ip}/ISAPI/System/deviceInfo"

# try:
#     response = requests.get(url, auth=HTTPDigestAuth(admin_user, admin_pass), timeout=5)
    
#     if response.status_code == 200:
#         print("Conneted Successfully")
#         print("Camera Info :\n", response.text)
#     else:
#         print(f"Connection Error: {response.status_code}")

# except Exception as e:
#     print(f"حدث خطأ: {e}")



#==============================================================================================================================================================


# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET

# # --- Configuration ---
# ip = "10.175.0.62"
# user = "admin"
# pw = "IT@cam!@#"
# auth = HTTPDigestAuth(user, pw)
# ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}

# def get_hik_details():
#     try:
#         # 1. Get Serial Number
#         info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         r_info = requests.get(info_url, auth=auth, timeout=5)
        
#         # 2. Get MAC Address
#         net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
#         r_net = requests.get(net_url, auth=auth, timeout=5)

#         if r_info.status_code == 200 and r_net.status_code == 200:
#             # Parse Serial
#             root_info = ET.fromstring(r_info.content)
#             serial = root_info.find(".//ns:serialNumber", ns).text
            
#             # Parse MAC
#             root_net = ET.fromstring(r_net.content)
#             mac = root_net.find(".//ns:macAddress", ns).text
            
#             print(f"IP:     {ip}")
#             print(f"Serial: {serial}")
#             print(f"MAC:    {mac}")
        
#         elif r_info.status_code == 401:
#             print(f"Error: Unauthorized. Check username/password for {ip}")
#         else:
#             print(f"Error: Info Status {r_info.status_code} | Net Status {r_net.status_code}")

#     except Exception as e:
#         print(f"Connection Error for {ip}: {e}")

# get_hik_details()




#===========================================================================================================================================================
#Get only ip, serial and mac man

# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET

# # --- Configuration ---
# ip = "10.175.0.62"
# admin_user = "admin"
# admin_pass = "IT@cam!@#"

# def get_camera_details():
#     auth = HTTPDigestAuth(admin_user, admin_pass)
    
#     try:
#         # 1. Get Serial Number
#         info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         info_res = requests.get(info_url, auth=auth, timeout=5)
        
#         # 2. Get MAC Address
#         net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
#         net_res = requests.get(net_url, auth=auth, timeout=5)

#         if info_res.status_code == 200 and net_res.status_code == 200:
#             # Parse XML
#             root_info = ET.fromstring(info_res.content)
#             root_net = ET.fromstring(net_res.content)
            
#             # Using {*} to ignore namespaces - this prevents the 'NoneType' error
#             serial_tag = root_info.find(".//{*}serialNumber")
#             mac_tag = root_net.find(".//{*}macAddress")

#             # Check if tags actually exist before calling .text
#             serial = serial_tag.text if serial_tag is not None else "Not Found"
#             mac = mac_tag.text if mac_tag is not None else "Not Found"
            
#             print(f"IP:     {ip}")
#             print(f"Serial: {serial}")
#             print(f"MAC:    {mac}")
            
#         else:
#             print(f"Failed. HTTP Status: Info({info_res.status_code}), Net({net_res.status_code})")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# get_camera_details()



#===========================================================================================================================================================


# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# from concurrent.futures import ThreadPoolExecutor

# # --- CONFIGURATION ---
# # Add your subnets here (the first three octets)
# subnets = [
#     "10.175.0",
#     "10.175.57",
#     "192.168.1"
# ]

# admin_user = "admin"
# admin_pass = "IT@cam!@#"

# def scan_camera(ip):
#     auth = HTTPDigestAuth(admin_user, admin_pass)
#     timeout = 1.5  # Fast timeout for scanning
    
#     try:
#         # 1. Get Serial Number
#         info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         r_info = requests.get(info_url, auth=auth, timeout=timeout)
        
#         if r_info.status_code == 200:
#             # 2. Get MAC Address
#             net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
#             r_net = requests.get(net_url, auth=auth, timeout=timeout)
            
#             # Parse XML using wildcards to avoid NoneType errors
#             root_info = ET.fromstring(r_info.content)
#             serial_tag = root_info.find(".//{*}serialNumber")
#             serial = serial_tag.text if serial_tag is not None else "Unknown"
            
#             mac = "Unknown"
#             if r_net.status_code == 200:
#                 root_net = ET.fromstring(r_net.content)
#                 mac_tag = root_net.find(".//{*}macAddress")
#                 mac = mac_tag.text if mac_tag is not None else "Unknown"
            
#             return f"{ip:<15} | {mac:<18} | {serial}"
#     except:
#         pass
#     return None

# # --- EXECUTION ---
# print(f"{'IP Address':<15} | {'MAC Address':<18} | {'Serial Number'}")
# print("-" * 60)

# for subnet in subnets:
#     print(f"\n>>> Walking Subnet: {subnet}.x")
#     # Generate IPs .1 to .255 for the current subnet
#     ips = [f"{subnet}.{i}" for i in range(1, 256)]
    
#     # Using ThreadPool to scan 30 IPs at a time for speed
#     with ThreadPoolExecutor(max_workers=30) as executor:
#         results = executor.map(scan_camera, ips)
        
#         for res in results:
#             if res:
#                 print(res)

# print("\n--- All Subnets Scanned ---")
















# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# from concurrent.futures import ThreadPoolExecutor

# # --- CONFIGURATION ---
# subnets = [
#     "10.175.0",
#     "10.175.57",
#     "10.175.60" # Add as many as you need
# ]

# admin_user = "admin"
# admin_pass = "IT@cam!@#"

# def get_mac_address(ip, auth, timeout):
#     """Tries multiple common paths to find the MAC address."""
#     paths = [
#         f"http://{ip}/ISAPI/System/Network/interfaces/1",
#         f"http://{ip}/ISAPI/System/Network/interfaces/2",
#         f"http://{ip}/ISAPI/System/Network/interfaces/1/macAddress"
#     ]
    
#     for path in paths:
#         try:
#             r = requests.get(path, auth=auth, timeout=timeout)
#             if r.status_code == 200:
#                 # If the response is just the MAC string (some models do this)
#                 if ":" in r.text and len(r.text) < 20:
#                     return r.text.strip()
                
#                 # Otherwise parse XML
#                 root = ET.fromstring(r.content)
#                 mac_tag = root.find(".//{*}macAddress")
#                 if mac_tag is not None:
#                     return mac_tag.text
#         except:
#             continue
#     return "Not Found"

# def scan_camera(ip):
#     auth = HTTPDigestAuth(admin_user, admin_pass)
#     timeout = 2
    
#     try:
#         # 1. Get Serial Number
#         info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         r_info = requests.get(info_url, auth=auth, timeout=timeout)
        
#         if r_info.status_code == 200:
#             # Parse Serial
#             root_info = ET.fromstring(r_info.content)
#             serial_tag = root_info.find(".//{*}serialNumber")
#             serial = serial_tag.text if serial_tag is not None else "Unknown"
            
#             # 2. Hunt for MAC
#             mac = get_mac_address(ip, auth, timeout)
            
#             return f"{ip:<15} | {mac:<18} | {serial}"
#     except:
#         pass
#     return None

# # --- EXECUTION ---
# print(f"{'IP Address':<15} | {'MAC Address':<18} | {'Serial Number'}")
# print("-" * 80)

# for subnet in subnets:
#     print(f"\n>>> Scanning Subnet: {subnet}.x")
#     ips = [f"{subnet}.{i}" for i in range(1, 256)]
    
#     # max_workers=30 for high-speed multi-threading
#     with ThreadPoolExecutor(max_workers=30) as executor:
#         results = executor.map(scan_camera, ips)
        
#         for res in results:
#             if res:
#                 print(res)

# print("\n--- Scan Complete ---")















#============================================================================================================================================================
#============================================================================================================================================================
#============================================================================================================================================================
#The summary
#Single camera

# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# import re

# # --- Configuration ---
# ip = "10.175.0.62"
# admin_user = "admin"
# admin_pass = "IT@cam!@#"

# def get_camera_details():
#     auth = HTTPDigestAuth(admin_user, admin_pass)
    
#     try:
#         # 1. Get Serial Number
#         info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         info_res = requests.get(info_url, auth=auth, timeout=5)
        
#         # 2. Get Network Info (We try interface 1, which is standard)
#         net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
#         net_res = requests.get(net_url, auth=auth, timeout=5)

#         if info_res.status_code == 200:
#             # --- Extract Serial ---
#             root_info = ET.fromstring(info_res.content)
#             serial_tag = root_info.find(".//{*}serialNumber")
#             serial = serial_tag.text if serial_tag is not None else "Not Found"
            
#             # --- Extract MAC (Robust Search) ---
#             mac = "Not Found"
#             if net_res.status_code == 200:
#                 # We search for 'macAddress' OR 'physicalAddress' (used in some firmware)
#                 root_net = ET.fromstring(net_res.content)
#                 mac_tag = root_net.find(".//{*}macAddress") or root_net.find(".//{*}physicalAddress")
                
#                 if mac_tag is not None:
#                     mac = mac_tag.text
#                 else:
#                     # Fallback: Search the raw text for a MAC pattern if XML parsing fails
#                     mac_pattern = r'([0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2})'
#                     match = re.search(mac_pattern, net_res.text)
#                     if match:
#                         mac = match.group(1)

#             print(f"IP:     {ip}")
#             print(f"Serial: {serial}")
#             print(f"MAC:    {mac}")
            
#         else:
#             print(f"Failed. HTTP Status: Info({info_res.status_code})")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# get_camera_details()



#===================================================================================================================================================
#For a whole Subnet

# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# import re
# from concurrent.futures import ThreadPoolExecutor

# # --- Configuration ---
# subnet_prefix = "10.175.0"
# admin_user = "admin"
# admin_pass = "IT@cam!@#"

# def scan_camera(ip):
#     auth = HTTPDigestAuth(admin_user, admin_pass)
#     timeout = 2  # Time to wait for each IP
    
#     try:
#         # 1. Get Serial Number
#         info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         r_info = requests.get(info_url, auth=auth, timeout=timeout)
        
#         if r_info.status_code == 200:
#             # --- Extract Serial ---
#             root_info = ET.fromstring(r_info.content)
#             serial_tag = root_info.find(".//{*}serialNumber")
#             serial = serial_tag.text if serial_tag is not None else "Unknown"
            
#             # --- Extract MAC (Universal Hunt) ---
#             mac = "Not Found"
#             net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
#             r_net = requests.get(net_url, auth=auth, timeout=timeout)
            
#             if r_net.status_code == 200:
#                 # Attempt 1: Standard Tag
#                 root_net = ET.fromstring(r_net.content)
#                 mac_tag = root_net.find(".//{*}macAddress") or root_net.find(".//{*}physicalAddress")
                
#                 if mac_tag is not None:
#                     mac = mac_tag.text
#                 else:
#                     # Attempt 2: Regex search on raw text if tags fail
#                     mac_pattern = r'([0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2})'
#                     match = re.search(mac_pattern, r_net.text)
#                     if match:
#                         mac = match.group(1)

#             return f"{ip:<15} | {mac:<18} | {serial}"
#     except:
#         # Silently skip IPs that don't respond
#         pass
#     return None

# # --- Main Execution ---
# print(f"Starting Scan on {subnet_prefix}.1 to {subnet_prefix}.255...")
# print(f"{'IP Address':<15} | {'MAC Address':<18} | {'Serial Number'}")
# print("-" * 80)

# # Generate list of IPs
# ips = [f"{subnet_prefix}.{i}" for i in range(1, 256)]

# # Use 30 threads for high speed (scans the whole subnet in ~20 seconds)
# with ThreadPoolExecutor(max_workers=30) as executor:
#     results = executor.map(scan_camera, ips)
    
#     for res in results:
#         if res:
#             print(res)

# print("-" * 80)
# print("Scan Complete.")


#================================================================================================================================================================
#create csv file for the results

# import requests
# from requests.auth import HTTPDigestAuth
# import xml.etree.ElementTree as ET
# import re
# import csv
# from concurrent.futures import ThreadPoolExecutor

# # --- CONFIGURATION ---
# subnet_prefix = "10.175.0"
# admin_user = "admin"
# admin_pass = "IT@cam!@#"
# output_file = "camera_results.csv"

# def scan_camera(ip):
#     auth = HTTPDigestAuth(admin_user, admin_pass)
#     timeout = 2
    
#     try:
#         # 1. Get Serial Number
#         info_url = f"http://{ip}/ISAPI/System/deviceInfo"
#         r_info = requests.get(info_url, auth=auth, timeout=timeout)
        
#         if r_info.status_code == 200:
#             # Extract Serial
#             root_info = ET.fromstring(r_info.content)
#             serial_tag = root_info.find(".//{*}serialNumber")
#             serial = serial_tag.text if serial_tag is not None else "Unknown"
            
#             # 2. Get MAC Address (Universal Hunt)
#             mac = "Not Found"
#             net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
#             r_net = requests.get(net_url, auth=auth, timeout=timeout)
            
#             if r_net.status_code == 200:
#                 root_net = ET.fromstring(r_net.content)
#                 mac_tag = root_net.find(".//{*}macAddress") or root_net.find(".//{*}physicalAddress")
                
#                 if mac_tag is not None:
#                     mac = mac_tag.text
#                 else:
#                     # Regex fallback for tricky models
#                     mac_pattern = r'([0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2})'
#                     match = re.search(mac_pattern, r_net.text)
#                     if match:
#                         mac = match.group(1)

#             # Return as a dictionary for the CSV writer
#             return {"IP Address": ip, "MAC Address": mac, "Serial Number": serial}
#     except:
#         pass
#     return None

# # --- EXECUTION ---
# print(f"Scanning {subnet_prefix}.1 to .255...")
# ips = [f"{subnet_prefix}.{i}" for i in range(1, 256)]
# found_cameras = []

# # Use 30 threads for speed
# with ThreadPoolExecutor(max_workers=30) as executor:
#     results = executor.map(scan_camera, ips)
#     for res in results:
#         if res:
#             found_cameras.append(res)
#             print(f"Found: {res['IP Address']} | {res['MAC Address']}")

# # Write to CSV
# if found_cameras:
#     keys = found_cameras[0].keys()
#     with open(output_file, 'w', newline='') as f:
#         dict_writer = csv.DictWriter(f, fieldnames=keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(found_cameras)
#     print(f"\nSuccess! {len(found_cameras)} cameras saved to {output_file}")
# else:
#     print("\nNo cameras found.")


#============================================================================================================================================\


import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
import re
import csv
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
subnet_prefix = "10.175.57"
admin_user = "admin"
admin_pass = "IT@cam!@#"
output_file = "camera_results.csv"

def scan_camera(ip):
    auth = HTTPDigestAuth(admin_user, admin_pass)
    timeout = 2
    
    try:
        # 1. Get Serial Number
        info_url = f"http://{ip}/ISAPI/System/deviceInfo"
        r_info = requests.get(info_url, auth=auth, timeout=timeout)
        
        if r_info.status_code == 200:
            # Extract Serial
            root_info = ET.fromstring(r_info.content)
            serial_tag = root_info.find(".//{*}serialNumber")
            serial = serial_tag.text if serial_tag is not None else "Unknown"
            
            # 2. Get MAC Address (Universal Hunt)
            mac = "Not Found"
            net_url = f"http://{ip}/ISAPI/System/Network/interfaces/1"
            r_net = requests.get(net_url, auth=auth, timeout=timeout)
            
            if r_net.status_code == 200:
                root_net = ET.fromstring(r_net.content)
                mac_tag = root_net.find(".//{*}macAddress") or root_net.find(".//{*}physicalAddress")
                
                if mac_tag is not None:
                    mac = mac_tag.text
                else:
                    # Regex fallback for tricky models
                    mac_pattern = r'([0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2})'
                    match = re.search(mac_pattern, r_net.text)
                    if match:
                        mac = match.group(1)

            # Return as a dictionary
            return {"IP Address": ip, "MAC Address": mac, "Serial Number": serial}
    except:
        pass
    return None

# --- EXECUTION ---
print(f"Scanning {subnet_prefix}.1 to .255...")
print(f"{'IP Address':<15} | {'MAC Address':<18} | {'Serial Number'}")
print("-" * 80)

ips = [f"{subnet_prefix}.{i}" for i in range(1, 256)]
found_cameras = []

with ThreadPoolExecutor(max_workers=30) as executor:
    results = executor.map(scan_camera, ips)
    for res in results:
        if res:
            found_cameras.append(res)
            # THIS LINE NOW PRINTS EVERYTHING TO THE TERMINAL
            print(f"{res['IP Address']:<15} | {res['MAC Address']:<18} | {res['Serial Number']}")

# Write to CSV
if found_cameras:
    keys = found_cameras[0].keys()
    with open(output_file, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(found_cameras)
    print("-" * 80)
    print(f"Success! {len(found_cameras)} cameras saved to {output_file}")
else:
    print("\nNo cameras found.")


