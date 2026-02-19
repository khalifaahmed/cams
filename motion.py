import requests
from requests.auth import HTTPDigestAuth

# --- Configuration ---
NVR_IP = "10.175.35.203"
USER = "admin"
PASS = "HQ@netcam!@#"

CHANNELS_TO_CHECK = list(range(1, 33))
# ---------------------

def set_motion(channel_id, enable=False):
    """
    Toggles motion detection. 
    enable=False to disable, enable=True to enable.
    """
    state = "false" if not enable else "true"
    url = f"http://{NVR_IP}/ISAPI/System/Video/inputs/channels/{channel_id}/motionDetection"
    
    # The exact payload that worked in your cURL test
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
        # We use a short timeout so the script doesn't hang on empty channels
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
            # This channel likely doesn't exist on this NVR
            pass 
        else:
            print(f"[!] Channel {channel_id}: Received status {response.status_code}")
            
    except requests.exceptions.RequestException:
        # Likely a timeout or connection issue for this specific channel
        pass

if __name__ == "__main__":
    action = "DISABLING"
    print(f"Starting: {action} motion on NVR {NVR_IP}...")
    
    for ch in CHANNELS_TO_CHECK:
        set_motion(ch, enable=False)
        
    print("Done.")