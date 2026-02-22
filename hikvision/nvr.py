import requests
from requests.auth import HTTPDigestAuth

# Device Details
ip_address = "10.175.0.203"
admin_user = "admin"
admin_pass = "HQ@netcam!@#"
target_id = "20"  # The User ID we are configuring

# Total cameras on your NVR (adjust if you have a 16, 32, or 64 channel unit)
total_channels = 32 

url = f"http://{ip_address}/ISAPI/Security/users/{target_id}"

# Generate the XML blocks for ALL cameras dynamically
permission_blocks = ""
for cam_id in range(1, total_channels + 1):
    permission_blocks += f"""
        <UserChannelPermission>
            <id>{cam_id}</id>
            <remoteLiveView>true</remoteLiveView>
            <remotePlayback>true</remotePlayback>
            <remotePTZControl>true</remotePTZControl>
        </UserChannelPermission>"""

# The Full XML Payload
xml_payload = f"""<User version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
    <id>{target_id}</id>
    <userName>AllCameraUser</userName>
    <password>Security123!</password>
    <userLevel>Operator</userLevel>
    <UserChannelPermissionList>
        {permission_blocks}
    </UserChannelPermissionList>
</User>"""

try:
    response = requests.put(
        url, 
        data=xml_payload, 
        auth=HTTPDigestAuth(admin_user, admin_pass),
        headers={'Content-Type': 'application/xml'}
    )

    if response.status_code == 200:
        print(f"Success! User {target_id} now has Live/Playback access to all {total_channels} cameras.")
    else:
        print(f"Failed. Status: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Connection Error: {e}")








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


