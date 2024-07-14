import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
from pyodide.http import open_url
#import hvplot.pandas
#import numpy as np
import json
from js import Bokeh, JSON
import pandas as pd
#import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.embed import json_item
#import panel as pn
from pyscript import display, when, document, window
from cryptography.fernet import Fernet, InvalidToken
#from js import localStorage

base_url='https://docs.google.com/spreadsheets/d/'
salt='6GQSdKCJNenmpL26muvRGlwTSoBI0A=='
encrypted_key=b'gAAAAABmkkAeROlTrwWwEEZQXoCfFHwbbyzN4sZT6Gt9blB86pvwcaL4tiroqlRD1uJOqIuBnJdzdXZNAhhcFc8kzFTNMYv9y0XSIvZkdsyKJa9ro4aura-qYJBQlEDlcViX-CWcPoFn'

URL_sensorNames_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=sensorNames&range=A:B'
URL_CSV_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=dataLogs&range=A:J'
URL_warn_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=warnings&range=A1'
URL_login = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=warnings&range=A20'
URL_lastEntry_aff = "/gviz/tq?tqx=out:csv;outFileName:data&sheet=last_entry&range=A:K"
page_ID=''

User=document.getElementById("uname")

Can_access=0

#<textarea id="uname"></textarea>
if window.localStorage.getItem("UserName"):
    User.value=window.localStorage.getItem("UserName")
#    User.value=localStorage.getItem("UserName")
    User.defaultValue=window.localStorage.getItem("UserName")

@when("click", "#login_submit")
def authenticate(event):
    global Can_access, page_ID, URL_sensorNames, URL_CSV, URL_warn, URL_lastEntry, names_data, warnings_data, last_entry
    global URL_sensorNames_aff, URL_CSV_aff, URL_warn_aff, URL_lastEntry_aff, sensor_select_parent
    valid_text=User.value
    if valid_text=="":
        window.alert("برای استفاده از نرم‌افزار گذرواژه خود را وارد کنید")
    else:
        if len(valid_text)==13:
            Can_access=-1
            secret_key=str.encode(valid_text+salt)
            fernet=Fernet(secret_key)
            try:
                page_ID=fernet.decrypt(encrypted_key).decode()
            except InvalidToken:
                page_ID=""
                Can_Access=0
                window.alert("گذرواژه نادرست است")
        if Can_access==-1 and pd.read_csv(open_url(base_url+page_ID+URL_login), header=None)[0].to_list()[0]==1:
            Can_access=1
            display("خوش آمدید", target="temp_check")
            URL_sensorNames=base_url+page_ID+URL_sensorNames_aff
            URL_CSV=base_url+page_ID+URL_CSV_aff
            URL_warn=base_url+page_ID+URL_warn_aff
            URL_lastEntry=base_url+page_ID+URL_lastEntry_aff
            names_data=pd.read_csv(open_url(URL_sensorNames))
            warnings=pd.read_csv(open_url(URL_warn))
            warnings2=[int(x) for x in warnings.columns[0].split(',') if x!=' ']
            warnings_data=", ".join(list(names_data[names_data.ID.isin(warnings2)].Name))
            last_entry=pd.read_csv(open_url(URL_lastEntry))

            sensor_select_parent=document.querySelector('#sensor-select')
            for x in names_data.Name:
                sel_item = document.createElement("option")
                sel_item.textContent = x
                sensor_select_parent.appendChild(sel_item)
            checkbox=document.getElementById("rememberMe")
            if checkbox.checked:
                window.localStorage.setItem("UserName", valid_text)
        else:
            window.alert("گذرواژه نادرست است")


@when("click", "#update")
def click_handler(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    global sensor_select_parent
    if Can_access>0:

        temp=last_entry[last_entry.ID==names_data[names_data.Name==sensor_select_parent.value].ID.iloc[0]]
        report='Date: '+str(temp.DateTime.iloc[0])+', EC: '+str(temp.aquaEC.iloc[0])+', CO: '+str(temp.CO.iloc[0])+', T: '+str(temp.Temperature.iloc[0])+', RH: '+str(temp.RH.iloc[0])+', Lux:'+str(temp.Luminosity.iloc[0])

        element=document.getElementById("parrot1")
        element.innerHTML = warnings_data
        element2=document.getElementById("parrot2")
        element2.innerHTML = report
    else:
        window.alert("برای استفاده از نرم‌افزار گذرواژه خود را وارد کنید")
#select = pn.widgets.Select(name='انتخاب حسگر', options=[x for x in names_data.Name]).servable(target='sensor-select')

from_date=document.getElementById("start_date")
end_date=document.getElementById("end_date")

@when("click", "#fetch")
def handle_click(event):
#    element.write(from_date.value)
    if Can_access>0:
        if from_date.value=="2024-01-01" and end_date.value=="2024-01-01":
            window.alert("لطفا ابتدا تاریخ ابتدا و انتهای بازه را تعیین کنید")
        elif pd.to_datetime(from_date.value)>pd.to_datetime(end_date.value):
            window.alert("تاریخ انتهای بازه باید بزرگتر از تاریخ ابتدا باشد")
        else:
            orig_data=pd.read_csv(open_url(URL_CSV))
            orig_data=orig_data[orig_data['Time'].notna()]
            selected_ID=names_data[names_data.Name==sensor_select_parent.value].ID.iloc[0].item()
            plt_data=orig_data[orig_data.ID==selected_ID].copy()
            plt_data['DateTime']=pd.to_datetime(plt_data['Date']+' '+plt_data['Time'], format='mixed')
            plt_data=plt_data.drop(['Date', 'Time'], axis=1)
            plt_data=plt_data[plt_data.DateTime>=pd.to_datetime(from_date.value)]
            plt_data=plt_data[plt_data.DateTime<=pd.to_datetime(end_date.value)]
            if selected_ID<2000:
                p1=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="Temperature [°C]", x_axis_label="DateTime")
                p1.line(plt_data['DateTime'], plt_data['Temperature [C]'], line_width=2, alpha=0.8)
                p2=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="Relative Humidity[%]", x_axis_label="DateTime")
                p2.line(plt_data['DateTime'], plt_data['RH [%]'], line_width=2, alpha=0.8)
                p3=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="Luminosity [Lux]", x_axis_label="DateTime")
                p3.line(plt_data['DateTime'], plt_data['Luminosity [lux]'], line_width=2, alpha=0.8)
                p = column(p1, p2, p3)
                p_json = json.dumps(json_item(p, "plotResults"))
                Bokeh.embed.embed_item(JSON.parse(p_json))
            elif selected_ID>=4000:
                p=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="CO [ppm]", x_axis_label="DateTime")
                p.line(plt_data['DateTime'], plt_data['CO'], line_width=2, alpha=0.8)
                p_json = json.dumps(json_item(p, "plotResults"))
                Bokeh.embed.embed_item(JSON.parse(p_json))
            else:
                p=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="EC [ugr/ml]", x_axis_label="DateTime")
                p.line(plt_data['DateTime'], plt_data['aquaEC'], line_width=2, alpha=0.8)
                p_json = json.dumps(json_item(p, "plotResults"))
                Bokeh.embed.embed_item(JSON.parse(p_json))
    else:
        window.alert("برای استفاده از نرم‌افزار گذرواژه خود را وارد کنید")

