import requests
from requests.auth import HTTPDigestAuth

# --- CONFIGURATION ---
NVR_IP = "10.175.0.203"
ADMIN_USER = "admin"
ADMIN_PASS = "HQ@netcam!@#"

TARGET_ID = "20"
TARGET_NAME = "ViewerUser"
TARGET_PASS = "UserPassword123"
TOTAL_CHANNELS = 16 

def generate_wide_channel_list():
    """Generates permissions for IDs 1-64 (Analog/IP mix)"""
    xml = ""
    for i in range(1, 65):
        xml += f"""
        <ChannelPermission>
            <id>{i}</id>
            <preview>true</preview>
            <playBack>true</playBack>
        </ChannelPermission>"""
    return xml

def update_permissions():
    url = f"http://{NVR_IP}/ISAPI/Security/users/{TARGET_ID}"
    
    channels = generate_wide_channel_list()

    # This structure covers Remote, Local, and explicit Channel Permissions
    xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<User version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
    <id>{TARGET_ID}</id>
    <userName>{TARGET_NAME}</userName>
    <password>{TARGET_PASS}</password>
    <userLevel>User</userLevel>
    <UserPermission>
        <remotePermission>
            <preview>true</preview>
            <playBack>true</playBack>
            <logQuery>false</logQuery>
            <config>false</config>
            <ptzControl>false</ptzControl>
            <upgrade>false</upgrade>
            <voiceTalk>false</voiceTalk>
            <reboot>false</reboot>
            <setupParameters>false</setupParameters>
            <shellAccess>false</shellAccess>
        </remotePermission>
        <localPermission>
            <preview>true</preview>
            <playBack>true</playBack>
        </localPermission>
        <ChannelPermissionList>
            {channels}
        </ChannelPermissionList>
    </UserPermission>
</User>"""

    headers = {'Content-Type': 'application/xml'}

    try:
        response = requests.put(
            url, 
            data=xml_data, 
            headers=headers, 
            auth=HTTPDigestAuth(ADMIN_USER, ADMIN_PASS),
            timeout=10
        )

        if response.status_code == 200:
            print(f"Update sent to User {TARGET_ID}...")
            # Verification Step:
            print("--- VERIFYING ACTUAL SETTINGS ---")
            check = requests.get(url, auth=HTTPDigestAuth(ADMIN_USER, ADMIN_PASS))
            print(check.text)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Conn Error: {e}")

if __name__ == "__main__":
    update_permissions()




























# import requests
# from requests.auth import HTTPDigestAuth

# # --- Configuration ---
# NVR_IP = "10.175.0.203"
# ADMIN_USER = "admin"
# ADMIN_PASS = "HQ@netcam!@#"



# TARGET_ID = "20"
# TARGET_NAME = "ViewerUser"
# TARGET_PASS = "UserPassword123"

# def update_user_permissions():
#     url = f"http://{NVR_IP}/ISAPI/Security/users/{TARGET_ID}"
    
#     # Defining permissions for Channel 1 and Channel 2 specifically
#     # Add more <ChannelPermission> blocks as needed for your NVR
#     xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
# <User version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
#     <id>{TARGET_ID}</id>
#     <userName>{TARGET_NAME}</userName>
#     <password>{TARGET_PASS}</password>
#     <userLevel>User</userLevel>
#     <UserPermission>
#         <remotePermission>
#             <preview>true</preview>
#             <playBack>true</playBack>
#             <logQuery>false</logQuery>
#             <config>false</config>
#             <ptzControl>false</ptzControl>
#             <upgrade>false</upgrade>
#             <voiceTalk>false</voiceTalk>
#             <reboot>false</reboot>
#             <setupParameters>false</setupParameters>
#             <shellAccess>false</shellAccess>
#         </remotePermission>
#         <ChannelPermissionList>
#             <ChannelPermission>
#                 <id>1</id>
#                 <preview>true</preview>
#                 <playBack>true</playBack>
#             </ChannelPermission>
#             <ChannelPermission>
#                 <id>2</id>
#                 <preview>true</preview>
#                 <playBack>true</playBack>
#             </ChannelPermission>
#         </ChannelPermissionList>
#     </UserPermission>
# </User>"""

#     headers = {'Content-Type': 'application/xml'}

#     try:
#         response = requests.put(
#             url, 
#             data=xml_data, 
#             headers=headers, 
#             auth=HTTPDigestAuth(ADMIN_USER, ADMIN_PASS),
#             timeout=10
#         )

#         if response.status_code == 200:
#             print(f"Success! User {TARGET_NAME} is now a 'User' with Live/Playback on Ch 1 & 2.")
#         else:
#             print(f"Failed: {response.status_code}")
#             print(response.text)

#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     update_user_permissions()
















# import requests
# from requests.auth import HTTPDigestAuth

# # Device Details
# ip_address = "10.175.0.203"
# admin_user = "admin"
# admin_pass = "HQ@netcam!@#"
# target_id = "20"  # The User ID we are configuring

# # Total cameras on your NVR (adjust if you have a 16, 32, or 64 channel unit)
# total_channels = 32 

# url = f"http://{ip_address}/ISAPI/Security/users/{target_id}"

# # Generate the XML blocks for ALL cameras dynamically
# permission_blocks = ""
# for cam_id in range(1, total_channels + 1):
#     permission_blocks += f"""
#         <UserChannelPermission>
#             <id>{cam_id}</id>
#             <remoteLiveView>true</remoteLiveView>
#             <remotePlayback>true</remotePlayback>
#             <remotePTZControl>true</remotePTZControl>
#         </UserChannelPermission>"""

# # The Full XML Payload
# xml_payload = f"""<User version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
#     <id>{target_id}</id>
#     <userName>AllCameraUser</userName>
#     <password>Security123!</password>
#     <userLevel>Operator</userLevel>
#     <UserChannelPermissionList>
#         {permission_blocks}
#     </UserChannelPermissionList>
# </User>"""

# try:
#     response = requests.put(
#         url, 
#         data=xml_payload, 
#         auth=HTTPDigestAuth(admin_user, admin_pass),
#         headers={'Content-Type': 'application/xml'}
#     )

#     if response.status_code == 200:
#         print(f"Success! User {target_id} now has Live/Playback access to all {total_channels} cameras.")
#     else:
#         print(f"Failed. Status: {response.status_code}")
#         print(response.text)
        
# except Exception as e:
#     print(f"Connection Error: {e}")








# import requests
# from requests.auth import HTTPDigestAuth


# ip_address = "10.175.0.203"
# admin_user = "admin"
# admin_pass = "HQ@netcam!@#"


# user_id = "20"
# url = f"http://{ip_address}/ISAPI/Security/users/{user_id}"

# xml_data = f"""
# <User version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
#     <id>{user_id}</id>
#     <userName>SecurityTeam</userName>
#     <password>SecurityPass2024!</password>
#     <userLevel>User</userLevel>
# </User>
# """

# try:
#     response = requests.put(
#         url, 
#         data=xml_data, 
#         auth=HTTPDigestAuth(admin_user, admin_pass),
#         headers={'Content-Type': 'application/xml'}
#     )

#     if response.status_code == 200:
#         print("User added successfully!")
#     else:
#         print(f"Failed. Status Code: {response.status_code}")
#         print(response.text)
# except Exception as e:
#     print(f"An error occurred: {e}")


