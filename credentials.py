import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
from pyscript import display, when, document, window
from cryptography.fernet import Fernet, InvalidToken

salt='SdKCJNenmpL26muvRGlwTSoBI0A=='
encrypted_key=[b'gAAAAABn47eFX59vp8F3yx0H4Ytwdplmy6Cxo40s-qhZS9lEMeyACHRpv7sgx_tCO-4bJUtf3fm7u_vV0r79oCXoLM6sGTRIYBb_EtbiflzWW7pcLDOwyXNIS2Kj16oLMcTLa93dddDo', b'gAAAAABn47eFGdtDWtwXSuiyNbTAn8Pk82Rw0nBb32kr8da_9LYB4aFW033EYJqlBCTf54aCUBDMKNb-YgdGi0osZS1jGKTRkAJqCh4b6Rio3y_n95cJ0XltAYAPH2hHvZkGUfjSzXpb', b'gAAAAABn47eFcXoFgQ_KHS0KIsS_wJdaNBIlZm4V_bRIBtyO5lV0HyxtPrexZEJC6F6TQkbGmBP5S7zOa3uUz8o0CNVvgcz7kEd84e2ohG74bJy_x4Sig2sVwb092eB0J5q_HjpbfFPR', b'gAAAAABn47eFuI5uWIZpeCJQPUIHqNkrIOWJziImaqnLjiRf6ZkYsgc1TWOLD5xhuPKgusyHx2iD5LJzjEY3D9Cx8HIVF3Vzf8k6rjNDKJD6fiLB7efQ9Ei2oBkkbRTl4FqDM0FtgPA7', b'gAAAAABn47eFq2hHjz5KitssFUbwZoewzqo0UUbm2M50TZGKGjZs3ERlFqxTgbkI_3-Or2DNlWRdLQ1T4wMCeSB-p8029-68ttVFNW2azTqhAa_3vU3Q3hTzlx-YJYucK4uxVmYFBtss', b'gAAAAABn47eFtgZyKEf69fna_Gl8-0qvtPeJX0HdfxshMdMeIpDrDNB0nYe0yK-m00TSbZByOeLddBJvdqUCvnuw3q3EcSi8Zq41kQhNtVMMiBFM1tNxDiVdnrFHbdP4pPC2g7oRxT1g']


User=document.getElementById("uname")


if window.localStorage.getItem("UserName"):
    User.value=window.localStorage.getItem("UserName")
    User.defaultValue=window.localStorage.getItem("UserName")

@when("click", "#login_submit")
def authenticate(event):
    valid_text=User.value.ljust(16,'0')
    page_ID=""
    employee=""
    if valid_text=="":
        window.alert("برای استفاده از نرم‌افزار گذرواژه خود را وارد کنید")
    else:
        secret_key=str.encode(valid_text+salt)
        fernet=Fernet(secret_key)
        for j, i in enumerate(encrypted_key):
            try:
                page_ID=fernet.decrypt(i).decode()
                employee=str(j)
            except InvalidToken:
                page_ID=""
                employee=""
            except:
                page_ID=""
                employee=""
            if len(page_ID)>1:
                break
        if len(page_ID)>1:
            display("خوش آمدید", target="temp_check")
            checkbox=document.getElementById("rememberMe")
            if checkbox.checked:
                window.localStorage.setItem("UserName", valid_text)
            document.location.href="main_app.html?"+page_ID+","+employee
        else:
            window.alert("گذرواژه نادرست است")
