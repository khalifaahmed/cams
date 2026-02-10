import requests
from requests.auth import HTTPDigestAuth

ip = "10.175.0.62"
admin_user = "admin"
admin_pass = "IT@cam!@#"

# مسار تفعيل البروتوكولات المدمجة
url_enable = f"http://{ip}/ISAPI/System/Network/Integrate"

xml_enable = """<Integrate version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
    <ONVIF>
        <enable>true</enable>
    </ONVIF>
</Integrate>"""

response = requests.put(url_enable, auth=HTTPDigestAuth(admin_user, admin_pass), data=xml_enable)
print(f"ONVIF activated: {response.status_code}")   




# مسار إضافة مستخدم أون فيف
url_add_user = f"http://{ip}/ISAPI/Security/ONVIF/users"

# الهيكل ده هو اللي الكاميرا بتطلبه في الموديلات الجديدة
xml_user = f"""<OnvifUser version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
    <id>5</id>
    <userName>onvif_admin</userName>
    <password>Pass123456!</password>
    <userLevel>Administrator</userLevel>
</OnvifUser>"""

headers = {'Content-Type': 'application/xml'}
response = requests.post(url_add_user, 
                         auth=HTTPDigestAuth(admin_user, admin_pass), 
                         data=xml_user, 
                         headers=headers)

if response.status_code in [200, 201]:
    print("ONVIF user add successfully ✅!")
else:
    print(f"❌ فشل الإضافة: {response.status_code}")
    print(response.text)




def add_camera_user(new_username, new_password, role="Operator"):
    url = f"http://{ip}/ISAPI/Security/users"
    
    # Hikvision User XML Schema
    # ID '2' is typically the first available slot after the default admin
    user_xml = f"""<User version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
        <id>2</id>
        <userName>{new_username}</userName>
        <password>{new_password}</password>
        <userLevel>{role}</userLevel>
    </User>"""

    headers = {'Content-Type': 'application/xml'}

    try:
        response = requests.post(
            url, 
            auth=HTTPDigestAuth(admin_user, admin_pass), 
            data=user_xml, 
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200 or response.status_code == 201:
            print(f"User '{new_username}' created successfully.")
        else:
            print(f"Failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

# Execute
add_camera_user("AAA2", "poiiop!@#", "Operator")









# import requests
# from requests.auth import HTTPDigestAuth

# ip = "10.175.0.133"
# admin_user = "admin"
# admin_pass = "IT@cam!@#"

# # هنستخدم ID رقم 3
# url = f"http://{ip}/ISAPI/Security/ONVIF/users"

# # الهيكل ده هو "المعيار الذهبي" لهيكفيشن حالياً
# xml_data = f"""<OnvifUser version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
#     <id>4</id>
#     <userName>Developer</userName>
#     <password>Pass123456!</password>
#     <userLevel>Administrator</userLevel>
# </OnvifUser>"""

# try:
#     headers = {'Content-Type': 'application/xml'}
#     response = requests.post(url, 
#                              auth=HTTPDigestAuth(admin_user, admin_pass), 
#                              data=xml_data, 
#                              headers=headers)
    
#     if response.status_code in [200, 201]:
#         print("✅ تم إضافة مستخدم الـ ONVIF بنجاح!")
#     else:
#         print(f"❌ خطأ {response.status_code}: {response.text}")
# except Exception as e:
#     print(f"Error: {e}")









# import requests
# from requests.auth import HTTPDigestAuth

# # بيانات الكاميرا
# ip_address = "10.175.0.133"
# username = "admin"
# password = "IT@cam!@#"

# # المسار الخاص بمعلومات الجهاز في بروتوكول ISAPI
# url = f"http://10.175.0.134/ISAPI/System/deviceInfo"

# try:
#     # إرسال الطلب باستخدام Digest Authentication (النظام اللي بتستخدمه هيكفيشن)
#     response = requests.get(url, auth=HTTPDigestAuth(username, password), timeout=5)
    
#     if response.status_code == 200:
#         print("تم الاتصال بنجاح!")
#         print("بيانات الكاميرا:\n", response.text)
#     else:
#         print(f"خطأ في الاتصال. كود الخطأ: {response.status_code}")

# except Exception as e:
#     print(f"حدث خطأ: {e}")



# # ------------------------------------------------------------

# import requests
# from requests.auth import HTTPDigestAuth

# ip = "10.175.0.134"
# admin_user = "admin"
# admin_pass = "IT@cam!@#"

# url = f"http://10.175.0.134/ISAPI/Security/users"

# response = requests.get(url, auth=HTTPDigestAuth(admin_user, admin_pass))
# print(response.text)

# -------------------------------------------------------------------------






#     ----------------------------------------------













# import requests
# from requests.auth import HTTPDigestAuth

# ip = "10.175.0.134"
# user = "admin"
# pw = "IT@cam!@#"

# url = f"http://{ip}/ISAPI/System/Network/Integrate"

# # الهيكل ده شامل كل البروتوكولات، أحياناً الكاميرا بترفض لو بعت ONVIF بس
# xml_full = """<?xml version="1.0" encoding="UTF-8"?>
# <Integrate version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
#     <ONVIF>
#         <enabled>true</enabled>
#     </ONVIF>
#     <CGI>
#         <enabled>true</enabled>
#         <certificateType>digest</certificateType>
#     </CGI>
# </Integrate>"""

# try:
#     # جربنا هنا PUT لأننا بنعدل حالة موجودة
#     response = requests.put(url, auth=HTTPDigestAuth(user, pw), data=xml_full, headers={'Content-Type': 'application/xml'})
#     print(f"Status Code: {response.status_code}")
#     print(f"Response: {response.text}")
# except Exception as e:
#     print(f"Error: {e}")