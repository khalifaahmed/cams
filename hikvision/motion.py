#!/usr/bin/python3

#Newer Version

import requests
from requests.auth import HTTPDigestAuth


NVR_IP = "10.175.24.203"
USER = "admin"
PASS = "HQ@netcam!@#"

CHANNELS_TO_CHECK = list(range(1, 33))


def set_motion(channel_id, enable=False):
    """
    Toggles motion detection. 
    enable=False to disable, enable=True to enable.
    """
    state = "false" if not enable else "true"
    url = f"http://{NVR_IP}/ISAPI/System/Video/inputs/channels/{channel_id}/motionDetection"
    

    payload = f"""<MotionDetection version='2.0'>
        <enabled>{state}</enabled>
        <enableHighlight>true</enableHighlight>
        <samplingInterval>5</samplingInterval>
        <startTriggerTime>1000</startTriggerTime>
        <endTriggerTime>1000</endTriggerTime>
        <regionType>grid</regionType>
        <Grid>
            <rowGranularity>18</rowGranularity>
            <columnGranularity>22</columnGranularity>
        </Grid>
        <MotionDetectionLayout>
            <sensitivityLevel>60</sensitivityLevel>
            <layout>
                <gridMap>fffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffc</gridMap>
            </layout>
            <targetType>human,vehicle</targetType>
        </MotionDetectionLayout>
    </MotionDetection>"""

    headers = {'Content-Type': 'application/xml'}
    
    try:
        response = requests.put(
            url, 
            data=payload, 
            auth=HTTPDigestAuth(USER, PASS), 
            headers=headers, 
            timeout=3 
        )
        
        if response.status_code == 200:
            print(f"[OK] Channel {channel_id}: Motion set to {state}")
        
        elif response.status_code == 404:
            pass 

        else:
            print(f"[!] Channel {channel_id}: Received status {response.status_code}")
            
    except requests.exceptions.RequestException:

        pass

if __name__ == "__main__":
    action = "DISABLING"
    print(f"Starting: {action} motion on NVR {NVR_IP}...")
    
    for ch in CHANNELS_TO_CHECK:
        set_motion(ch, enable=False)
        
    print("Done.")


#===================================================================================================================================================================


# #Old version (Borg Al Arab)

# import requests
# from requests.auth import HTTPDigestAuth

# NVR_IP = "10.175.24.202"
# USER = "admin"
# PASS = "HQ@netcam!@#"

# # Channels 1-32
# CHANNELS = list(range(1, 33))

# def disable_motion(channel_id):
#     url = f"http://{NVR_IP}/ISAPI/System/Video/inputs/channels/{channel_id}/motionDetection"
    
#     # This XML is built EXACTLY like the output you provided
#     payload = f"""<?xml version="1.0" encoding="UTF-8" ?>
# <MotionDetection version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
# <enabled>false</enabled>
# <samplingInterval>5</samplingInterval>
# <startTriggerTime>1000</startTriggerTime>
# <endTriggerTime>1000</endTriggerTime>
# <regionType>grid</regionType>
# <Grid>
# <rowGranularity>12</rowGranularity>
# <columnGranularity>16</columnGranularity>
# </Grid>
# <MotionDetectionLayout>
# <sensitivityLevel>0</sensitivityLevel>
# <layout>
# <gridMap>000000000000000000000000000000000000000000000000</gridMap>
# </layout>
# </MotionDetectionLayout>
# </MotionDetection>"""

#     headers = {'Content-Type': 'application/xml'}
    
#     try:
#         response = requests.put(
#             url, 
#             data=payload, 
#             auth=HTTPDigestAuth(USER, PASS), 
#             headers=headers, 
#             timeout=5
#         )
        
#         if response.status_code == 200:
#             print(f"[OK] Channel {channel_id}: Motion Disabled.")
#         elif response.status_code == 404:
#             pass # Channel not active
#         else:
#             print(f"[!] Channel {channel_id}: Status {response.status_code}")
#             print(response.text)
            
#     except Exception as e:
#         print(f"[X] Error: {e}")

# if __name__ == "__main__":
#     print(f"Starting disable process on {NVR_IP}...")
#     for ch in CHANNELS:
#         disable_motion(ch)
#     print("Done.")

































