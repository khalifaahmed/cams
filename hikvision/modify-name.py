import requests
from requests.auth import HTTPDigestAuth

def set_camera_name(ip, username, password, channel_id, new_name):
    # ISAPI URL for specific channel configuration
    url = f"http://{ip}/ISAPI/System/video/inputs/channels/{channel_id}"
    
    # XML Payload required by Hikvision ISAPI
    xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
    <videoInputChannel version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
        <id>{channel_id}</id>
        <inputPort>1</inputPort>
        <name>{new_name}</name>
    </videoInputChannel>
    """
    
    try:
        # Hikvision requires Digest Authentication
        response = requests.put(
            url, 
            data=xml_data, 
            auth=HTTPDigestAuth(username, password),
            headers={'Content-Type': 'application/xml'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Successfully updated channel {channel_id} to: {new_name}")
        else:
            print(f"Failed. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
CAM_IP = "10.175.0.134"
USER = "admin"
PASS = "IT@cam!@#"
CHANNEL = 1
NEW_NAME = "Camera-15"

set_camera_name(CAM_IP, USER, PASS, CHANNEL, NEW_NAME)