import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET


NVR_IP   = "10.175.0.203"
USERNAME = "admin"
PASSWORD = "HQ@netcam!@#"
# ---------------------

def get_camera_ips():
    url = f"http://{NVR_IP}/ISAPI/ContentMgmt/DeviceConfig/deviceList"
    
    try:
        response = requests.get(    
            url, 
            auth=HTTPDigestAuth(USERNAME, PASSWORD), 
            timeout=10
        )

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            devices = root.findall('.//{*}IDeviceConfig')
            
            print(f"{'ID':<5} | {'IP Address':<15} | {'Model/Name'}")
            print("-" * 40)
            
            ip_list = []
            for dev in devices:
                ip = dev.findtext('{*}ipAddress')
                dev_id = dev.findtext('{*}id')
                name = dev.findtext('{*}devName')

                if ip and ip != "0.0.0.0":
                    print(f"{dev_id:<5} | {ip:<15} | {name}")
                    ip_list.append(ip)
            
            return ip_list

        elif response.status_code == 401:
            print("Error: 401 Unauthorized. Check credentials or enable 'digest/basic' in NVR settings.")
        else:
            print(f"Error: Server returned status code {response.status_code}")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    ips = get_camera_ips()