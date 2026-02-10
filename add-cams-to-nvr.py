import requests
from requests.auth import HTTPDigestAuth

# -------- NVR INFO --------
nvr_ip = "10.175.0.203"
nvr_user = "admin"
nvr_pass = "HQ@netcam!@#"

# -------- CAMERA INFO --------
camera_ip = "10.175.0.105"
camera_user = "admin"
camera_pass = "IT@cam!@#"
channel_id = 21   # Channel number on NVR

url = f"http://{nvr_ip}/ISAPI/ContentMgmt/InputProxy/channels/{channel_id}"

xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<InputProxyChannel xmlns="http://www.isapi.org/ver20/XMLSchema">
    <id>{channel_id}</id>
    <enable>true</enable>
    <sourceInputPortDescriptor>
        <ipAddress>{camera_ip}</ipAddress>
        <managePortNo>8000</managePortNo>
        <userName>{camera_user}</userName>
        <password>{camera_pass}</password>
    </sourceInputPortDescriptor>
</InputProxyChannel>
"""

headers = {
    "Content-Type": "application/xml"
}

response = requests.put(
    url,
    data=xml_data.encode("utf-8"),
    headers=headers,
    auth=HTTPDigestAuth(nvr_user, nvr_pass)
)

print(response.status_code)
print(response.text)