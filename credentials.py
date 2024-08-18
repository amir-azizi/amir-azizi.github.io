import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
from pyscript import display, when, document, window
from cryptography.fernet import Fernet, InvalidToken

salt='6GQSdKCJNenmpL26muvRGlwTSoBI0A=='
encrypted_key=b'gAAAAABmkkAeROlTrwWwEEZQXoCfFHwbbyzN4sZT6Gt9blB86pvwcaL4tiroqlRD1uJOqIuBnJdzdXZNAhhcFc8kzFTNMYv9y0XSIvZkdsyKJa9ro4aura-qYJBQlEDlcViX-CWcPoFn'


User=document.getElementById("uname")


if window.localStorage.getItem("UserName"):
    User.value=window.localStorage.getItem("UserName")
    User.defaultValue=window.localStorage.getItem("UserName")

@when("click", "#login_submit")
def authenticate(event):
    valid_text=User.value
    page_ID=""
    if valid_text=="":
        window.alert("برای استفاده از نرم‌افزار گذرواژه خود را وارد کنید")
    else:
        secret_key=str.encode(valid_text+salt)
        fernet=Fernet(secret_key)
        try:
            page_ID=fernet.decrypt(encrypted_key).decode()
        except InvalidToken:
            page_ID=""
        except:
            page_ID=""
#        if Can_access==-1 and pd.read_csv(open_url(base_url+page_ID+URL_login), header=None)[0].to_list()[0]==1:
        finally:
            if len(page_ID)>1:
                display("خوش آمدید", target="temp_check")
                checkbox=document.getElementById("rememberMe")
                if checkbox.checked:
                    window.localStorage.setItem("UserName", valid_text)
                document.location.href="main_app.html?"+page_ID
            else:
                window.alert("گذرواژه نادرست است")
